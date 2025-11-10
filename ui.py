# -*- coding: utf-8 -*-
import ctypes
import datetime
import os
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QFrame

from design.ui_DuplicateWidget import Ui_Frame
from design.ui_MainWindow import Ui_MainWindow
from dff import DuplicateFileFinder, get_md5_hash, FileIgnoreList


class DuplicateWidget(QFrame):
    detail_template = "Размер файла: {} мб    Дата изменения: {}    Дата создания: {}    MD5 Хэш: {}"

    def __init__(self, files, parent=None, abs_path=""):
        self.file_1 = files[0]
        self.file_2 = files[1]

        super().__init__(parent)

        self.ui = Ui_Frame()
        self.ui.setupUi(self)

        self.ui.path_label.setText(os.path.relpath(self.file_1, abs_path))
        self.ui.path_label_2.setText(os.path.relpath(self.file_2, abs_path))

        self.ui.detail_label.setText(self.detail_template.format(*self.get_details(self.file_1)))
        self.ui.detail_label_2.setText(self.detail_template.format(*self.get_details(self.file_2)))

    @staticmethod
    def get_details(file):
        creation_timestamp = os.path.getctime(file)
        creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)
        formatted_time_1 = creation_datetime.strftime("%d.%m.%Y %H:%M:%S")

        creation_timestamp_2 = os.path.getmtime(file)
        creation_datetime_2 = datetime.datetime.fromtimestamp(creation_timestamp_2)
        formatted_time_2 = creation_datetime_2.strftime("%d.%m.%Y %H:%M:%S")

        md5_checksum = get_md5_hash(file)

        return round(os.path.getsize(file) / (1024 * 1024), 2), formatted_time_1, formatted_time_2, md5_checksum[-8:]


class MainWindow(QMainWindow):
    topic_template = "Всего файлов: {}    Сканировано файлов: {}    Просканированно: {:.2f} мб    Дубликатов найдено: {}"

    def __init__(self):
        super(MainWindow, self).__init__()

        self.DFF = DuplicateFileFinder()
        self.progress_text = ""

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.path_lineEdit.setText(os.path.abspath(os.curdir))
        self.ui.path_lineEdit.setText(r"F:\LFS\Фотография")

        self.ui.pathEdit_pushButton.clicked.connect(self.set_path)
        self.ui.scan_pushButton.clicked.connect(self.scan)
        # self.ui.moveToTrash_pushButton.clicked.connect(self.test)

        self.ui.topic_label.setText(self.topic_template.format(0, 0, 0, 0))

    def insert_progress(self, text, detailed, progress):
        QCoreApplication.processEvents()
        if not detailed or self.ui.detailProgress_checkBox.isChecked():
            self.progress_text += text + "\n"
            self.ui.progress_textEdit.setText(self.progress_text)

            for i in range(2):
                self.ui.progress_textEdit.update()
                cur_max = self.ui.progress_textEdit.verticalScrollBar().maximum()
                self.ui.progress_textEdit.verticalScrollBar().setValue(cur_max)

            self.ui.topic_label.setText(
                self.topic_template.format(progress.total_files, progress.files_scanned, progress.megabytes_scanned,
                                           progress.duples_found))

            if progress.total_files:
                self.ui.progressBar.setValue(round(progress.files_scanned / progress.total_files * 100, 1))
                if progress.megabytes_to_scan:
                    self.ui.progressBar_2.setValue(
                        round(progress.megabytes_scanned / progress.megabytes_to_scan * 100, 1))

    def set_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Выберете путь", self.ui.path_lineEdit.text())
        if new_path is not None and new_path:
            self.ui.path_lineEdit.setText(new_path)

    def scan(self):

        self.ui.tabWidget.setCurrentIndex(0)

        self.ui.scan_pushButton.setEnabled(False)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar_2.setValue(0)
        self.progress_text = ""

        ignore_list = FileIgnoreList()
        ignore_list.ignore_string = self.ui.custom_ignore_lineEdit.text().strip()
        ignore_list.ignore_git = self.ui.skipGit_checkBox.isChecked()
        ignore_list.ignore_cache = self.ui.skipCache_checkBox.isChecked()
        ignore_list.ignore_system = self.ui.skipSystem_checkBox.isChecked()

        duplicates = self.DFF.find_duplicates(self.ui.path_lineEdit.text(),
                                              lambda t, d, p: self.insert_progress(t, d, p),
                                              ignore_list)

        while self.ui.verticalLayout_5.count():
            item = self.ui.verticalLayout_5.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()

        for dubs in duplicates:
            self.ui.verticalLayout_5.addWidget(DuplicateWidget(dubs, self, self.ui.path_lineEdit.text()))

        self.ui.progressBar.setValue(100)
        self.ui.progressBar_2.setValue(100)
        self.ui.scan_pushButton.setEnabled(True)

        self.ui.tabWidget.setCurrentIndex(1)


def main():
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    myappid = 'LinkCom.DFF.app.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    main()
