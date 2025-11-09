import hashlib
import os
import stat
import sys
import time
from typing import Dict, List, Callable, Optional, Tuple
from pathlib import Path


class DuplicateFileFinderConfig:
    """Класс конфигурации для поиска дубликатов файлов"""

    def __init__(self):
        # Флаги конфигурации
        self.verbose_output = False
        self.output_immediately = False
        self.trial_delete = False  # Пробный режим удаления (не удаляет файлы)
        self.delete_shorter = False  # Удалять файлы с более короткими именами

        # Константы
        self.BYTES_IN_A_MEGABYTE = 1048576
        self.BYTES_TO_SCAN = 4096  # Размер блока для чтения файла
        self.SCAN_SIZE_MB = self.BYTES_TO_SCAN / self.BYTES_IN_A_MEGABYTE


class ProgressTracker:
    """Класс для отслеживания прогресса сканирования"""

    def __init__(self):
        self.megabytes_scanned = 0.0
        self.failed_delete_count = 0
        self.progress_callback: Optional[Callable[[str, bool], None]] = None

    def set_progress_callback(self, callback: Callable[[str, bool], None]):
        """Устанавливает функцию обратного вызова для отображения прогресса"""
        self.progress_callback = callback

    def show_progress(self, message: str, verbose_only: bool = False):
        """Отображает прогресс выполнения"""
        if self.progress_callback:
            self.progress_callback(message, verbose_only)

    def add_scanned_bytes(self, bytes_count: int):
        """Добавляет количество просканированных байт"""
        self.megabytes_scanned += bytes_count / (1024 * 1024)

    def increment_failed_deletes(self):
        """Увеличивает счетчик неудачных удалений"""
        self.failed_delete_count += 1


class FileHashCalculator:
    """Класс для вычисления хешей файлов"""

    def __init__(self, config: DuplicateFileFinderConfig, progress: ProgressTracker):
        self.config = config
        self.progress = progress
        self.full_hashes: Dict[str, str] = {}

    def calculate_snippet_hash(self, file_path: str) -> str:
        """
        Вычисляет хеш первых BYTES_TO_SCAN байт файла

        Args:
            file_path: Путь к файлу

        Returns:
            Хеш в виде строки или сообщение об ошибке
        """
        self.progress.show_progress(f"...вычисление хеша фрагмента файла {file_path}", True)

        try:
            snip_hash = hashlib.blake2b()
            with open(file_path, "rb") as f:
                chunk = f.read(self.config.BYTES_TO_SCAN)
                if chunk:
                    snip_hash.update(chunk)
                    self.progress.add_scanned_bytes(len(chunk))
                return snip_hash.hexdigest()
        except PermissionError:
            error_msg = f"Ошибка доступа: {file_path}"
            self.progress.show_progress(error_msg, False)
            return f"PermissionError:{file_path}"
        except (OSError, IOError) as e:
            error_msg = f"Ошибка чтения файла {file_path}: {e}"
            self.progress.show_progress(error_msg, False)
            return f"IOError:{file_path}"

    def calculate_full_hash(self, file_path: str) -> str:
        """
        Вычисляет полный хеш файла

        Args:
            file_path: Путь к файлу

        Returns:
            Полный хеш файла
        """
        self.progress.show_progress(f"...вычисление полного хеша файла {file_path}", True)

        try:
            file_hash = hashlib.blake2b()
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(self.config.BYTES_TO_SCAN)
                    if not chunk:
                        break
                    file_hash.update(chunk)
                    self.progress.add_scanned_bytes(len(chunk))
            return file_hash.hexdigest()
        except (PermissionError, OSError, IOError) as e:
            error_msg = f"Ошибка при вычислении полного хеша {file_path}: {e}"
            self.progress.show_progress(error_msg, False)
            raise

    def find_duplicate_by_full_hash(self, snip_file_path: str, current_file_path: str) -> Optional[str]:
        """
        Ищет дубликат по полному хешу файла

        Args:
            snip_file_path: Путь к файлу с тем же хешем фрагмента
            current_file_path: Путь к текущему файлу

        Returns:
            Путь к дубликату или None, если дубликат не найден
        """
        try:
            # Вычисляем полный хеш текущего файла
            current_file_hash = self.calculate_full_hash(current_file_path)

            # Проверяем, есть ли уже файл с таким хешем
            if current_file_hash in self.full_hashes:
                return self.full_hashes[current_file_hash]

            # Вычисляем полный хеш файла с тем же хешем фрагмента
            snip_file_hash = self.calculate_full_hash(snip_file_path)
            self.full_hashes[snip_file_hash] = snip_file_path

            # Проверяем еще раз после добавления
            if current_file_hash in self.full_hashes:
                return self.full_hashes[current_file_hash]

            # Добавляем текущий файл в словарь
            self.full_hashes[current_file_hash] = current_file_path
            return None

        except Exception as e:
            self.progress.show_progress(f"Ошибка при поиске дубликата: {e}", False)
            return None


class FileSizeAnalyzer:
    """Класс для анализа размеров файлов и поиска потенциальных дубликатов"""

    def __init__(self, config: DuplicateFileFinderConfig, progress: ProgressTracker):
        self.config = config
        self.progress = progress
        self.size_to_file: Dict[int, str] = {}  # размер -> первый найденный файл
        self.files_to_process: Dict[str, bool] = {}  # файлы для дальнейшей обработки
        self.files_list: List[str] = []  # список файлов в порядке обхода
        self.total_files_count = 0

    def scan_directory(self, directory_path: str):
        """
        Сканирует директорию и находит файлы с одинаковыми размерами

        Args:
            directory_path: Путь к директории для сканирования
        """
        self.total_files_count = 0

        try:
            for root, _, files in sorted(os.walk(directory_path)):
                files.sort()
                for file_name in files:
                    self.total_files_count += 1
                    file_path = os.path.join(root, file_name)
                    self.progress.show_progress(f"Проверка размера файла {file_path}", True)

                    try:
                        file_size = os.path.getsize(file_path)
                        if file_size > 0:  # Игнорируем пустые файлы
                            self._process_file_size(file_path, file_size)
                    except (FileNotFoundError, OSError) as e:
                        # Возможно, символическая ссылка на несуществующий файл
                        self.progress.show_progress(f"Файл недоступен {file_path}: {e}", True)
                        continue
        except (PermissionError, OSError) as e:
            error_msg = f"Ошибка доступа к директории {directory_path}: {e}"
            self.progress.show_progress(error_msg, False)
            raise

    def _process_file_size(self, file_path: str, file_size: int):
        """
        Обрабатывает файл с определенным размером

        Args:
            file_path: Путь к файлу
            file_size: Размер файла
        """
        if file_size in self.size_to_file:
            # Найден файл с таким же размером
            self.progress.show_progress(
                f"{file_path} имеет неуникальный размер [{file_size} байт]", False
            )
            # Добавляем оригинальный файл в список для обработки
            self._add_original_file_to_process_list(self.size_to_file[file_size])
            # Добавляем текущий файл в список для обработки
            self._add_file_to_process_list(file_path)
        else:
            # Первый файл с таким размером
            self.size_to_file[file_size] = file_path

    def _add_original_file_to_process_list(self, original_file_path: str):
        """
        Добавляет оригинальный файл в список для обработки

        Args:
            original_file_path: Путь к оригинальному файлу
        """
        if original_file_path in self.files_to_process:
            self.progress.show_progress(f"{original_file_path} уже в списке дубликатов по размеру", True)
            return
        self._add_file_to_process_list(original_file_path)

    def _add_file_to_process_list(self, file_path: str):
        """
        Добавляет файл в список для дальнейшей обработки

        Args:
            file_path: Путь к файлу
        """
        self.files_to_process[file_path] = True
        self.files_list.append(file_path)
        self.progress.show_progress(f"{file_path} добавлен в список для обработки", True)


class DuplicateHandler:
    """Класс для обработки найденных дубликатов"""

    def __init__(self, config: DuplicateFileFinderConfig, progress: ProgressTracker):
        self.config = config
        self.progress = progress

    def display_duplicate(self, original_file: str, duplicate_file: str):
        """
        Отображает информацию о найденном дубликате

        Args:
            original_file: Путь к оригинальному файлу
            duplicate_file: Путь к файлу-дубликату
        """
        message = (
            f"            {duplicate_file}\n"
            f" является дубликатом {original_file}\n"
        )
        self.progress.show_progress(message, False)

    def delete_duplicate(self, original_file: str, duplicate_file: str) -> Tuple[str, str]:
        """
        Удаляет файл-дубликат

        Args:
            original_file: Путь к оригинальному файлу
            duplicate_file: Путь к файлу-дубликату

        Returns:
            Кортеж сообщений для оригинального и дублируемого файлов
        """
        file_to_delete = duplicate_file
        original_message = ""
        duplicate_message = "удален ... "

        if self.config.delete_shorter:
            # Удаляем файл с более коротким именем
            original_name = os.path.basename(original_file)
            duplicate_name = os.path.basename(duplicate_file)

            if len(original_name) < len(duplicate_name):
                file_to_delete = original_file
                original_message = " ... удален"
                duplicate_message = "            "

        if not self.config.trial_delete:
            try:
                # Убираем атрибут "только чтение" и удаляем файл
                os.chmod(file_to_delete, stat.S_IWRITE)
                os.remove(file_to_delete)
                self.progress.show_progress(f"Файл {file_to_delete} успешно удален", True)
            except FileNotFoundError:
                # Файл уже был удален
                original_message = " ... уже удален"
                self.progress.increment_failed_deletes()
            except (PermissionError, OSError) as e:
                error_msg = f"Ошибка при удалении файла {file_to_delete}: {e}"
                self.progress.show_progress(error_msg, False)
                self.progress.increment_failed_deletes()

        return original_message, duplicate_message


class OutputManager:
    """Класс для управления выводом"""

    def __init__(self):
        self.output_buffer = ""

    def unicode_safe_print(self, text: str):
        """
        Безопасный вывод текста с обработкой Unicode ошибок

        Args:
            text: Текст для вывода
        """
        try:
            print(text, flush=True)
            self.output_buffer += text + "\n"
        except UnicodeEncodeError:
            try:
                encoded_text = text.encode("utf8").decode(sys.stdout.encoding)
                print(encoded_text)
                self.output_buffer += encoded_text + "\n"
            except UnicodeDecodeError:
                safe_text = (
                        text.encode("utf8").decode(sys.stdout.encoding, errors="ignore")
                        + " <-- Ошибка кодировки Unicode"
                )
                print(safe_text)
                self.output_buffer += safe_text + "\n"

    def get_output(self) -> str:
        """Возвращает накопленный вывод"""
        return self.output_buffer


class DuplicateFileFinder:
    """Основной класс для поиска дубликатов файлов"""

    def __init__(self, config: Optional[DuplicateFileFinderConfig] = None):
        self.config = config or DuplicateFileFinderConfig()
        self.progress = ProgressTracker()
        self.output_manager = OutputManager()

        # Инициализируем компоненты
        self.file_size_analyzer = FileSizeAnalyzer(self.config, self.progress)
        self.hash_calculator = FileHashCalculator(self.config, self.progress)
        self.duplicate_handler = DuplicateHandler(self.config, self.progress)

    def find_duplicates(self, directory_path: str,
                        progress_callback: Optional[Callable[[str, bool], None]] = None) -> str:
        """
        Основной метод для поиска дубликатов файлов

        Args:
            directory_path: Путь к директории для сканирования
            progress_callback: Функция обратного вызова для отображения прогресса

        Returns:
            Строка с результатами поиска
        """
        if progress_callback:
            self.progress.set_progress_callback(progress_callback)
        else:
            # Устанавливаем стандартный обработчик прогресса
            self.progress.set_progress_callback(self._default_progress_handler)

        start_time = time.time()
        self.progress.show_progress(f"{time.strftime('%X')} : Начало поиска дубликатов", False)

        try:
            # Этап 1: Анализ размеров файлов
            self.file_size_analyzer.scan_directory(directory_path)

            # Этап 2: Поиск дубликатов по хешам
            duplicate_count = self._find_hash_duplicates()

            # Этап 3: Вывод статистики
            self._print_summary(duplicate_count, start_time)

            return self.output_manager.get_output()

        except Exception as e:
            error_msg = f"Критическая ошибка при поиске дубликатов: {e}"
            self.progress.show_progress(error_msg, False)
            raise

    def _find_hash_duplicates(self) -> int:
        """
        Поиск дубликатов по хешам среди файлов с одинаковыми размерами

        Returns:
            Количество найденных дубликатов
        """
        snippet_hashes: Dict[str, str] = {}
        duplicate_count = 0
        processed_files = 0

        for file_path in self.file_size_analyzer.files_list:
            processed_files += 1
            self.progress.show_progress(f"Обработка файла {file_path}", True)

            # Вычисляем хеш фрагмента файла
            snippet_hash = self.hash_calculator.calculate_snippet_hash(file_path)

            # Пропускаем файлы с ошибками
            if snippet_hash.startswith(("PermissionError:", "IOError:")):
                continue

            if snippet_hash in snippet_hashes:
                # Найден файл с таким же хешем фрагмента
                original_file = snippet_hashes[snippet_hash]
                duplicate_file_path = self.hash_calculator.find_duplicate_by_full_hash(original_file, file_path)

                if duplicate_file_path:
                    # Найден настоящий дубликат
                    self.duplicate_handler.display_duplicate(duplicate_file_path, file_path)
                    duplicate_count += 1
                else:
                    self.progress.show_progress(
                        "...первые 4096 байт одинаковы, но файлы различаются", True
                    )
            else:
                snippet_hashes[snippet_hash] = file_path

        return duplicate_count

    def _print_summary(self, duplicate_count: int, start_time: float):
        """
        Выводит итоговую статистику

        Args:
            duplicate_count: Количество найденных дубликатов
            start_time: Время начала работы
        """
        elapsed_time = round(time.time() - start_time, 3)

        summary = (
            f"\n{time.strftime('%X')} : "
            f"{duplicate_count} дубликатов найдено, "
            f"{len(self.file_size_analyzer.files_list)} файлов обработано, "
            f"{self.progress.megabytes_scanned:.2f} мегабайт просканировано за "
            f"{elapsed_time} секунд, "
            f"{self.file_size_analyzer.total_files_count} файлов проанализировано"
        )

        self.progress.show_progress(summary, False)

        if self.progress.failed_delete_count > 0:
            error_summary = f"\nНе удалось удалить {self.progress.failed_delete_count} дубликатов - запустите скрипт повторно"
            self.progress.show_progress(error_summary, False)

    def _default_progress_handler(self, message: str, verbose_only: bool):
        """
        Стандартный обработчик прогресса

        Args:
            message: Сообщение для вывода
            verbose_only: Показывать только в подробном режиме
        """
        if not verbose_only or self.config.verbose_output:
            self.output_manager.unicode_safe_print(message)


# Пример использования
if __name__ == "__main__":
    # Создаем конфигурацию
    config = DuplicateFileFinderConfig()
    config.verbose_output = True

    # Создаем экземпляр поисковика
    finder = DuplicateFileFinder(config)

    # Запускаем поиск
    try:
        result = finder.find_duplicates("C:\\temp")  # Замените на нужную директорию
        print("Поиск завершен успешно")
    except Exception as e:
        print(f"Ошибка при поиске дубликатов: {e}")