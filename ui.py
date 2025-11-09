# -*- coding: utf-8 -*-
import ctypes
import os
import sys
import datetime

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QFrame, QWidget

from design.ui_MainWindow import Ui_MainWindow
from design.ui_DuplicateWidget import Ui_Frame
from dff import DuplicateFileFinder, get_md5_hash


class DuplicateWidget(QFrame):
    detail_template = "Размер файла: {} мб    Дата изменения: {}    Дата создания: {}    MD5 Хэш: {}"

    def __init__(self, files, parent=None):

        self.file_1 = files[0]
        self.file_2 = files[1]

        super().__init__(parent)

        self.ui = Ui_Frame()
        self.ui.setupUi(self)

        self.ui.path_label.setText(self.file_1)
        self.ui.path_label_2.setText(self.file_2)

        self.ui.detail_label.setText(self.detail_template.format(*self.get_details(self.file_1)))
        self.ui.detail_label_2.setText(self.detail_template.format(*self.get_details(self.file_2)))

    @staticmethod
    def get_details(file):
        creation_timestamp = os.path.getctime(file)
        creation_datetime = datetime.datetime.fromtimestamp(creation_timestamp)
        formatted_time_1 = creation_datetime.strftime("%Y-%m-%d %H:%M:%S")

        creation_timestamp_2 = os.path.getmtime(file)
        creation_datetime_2 = datetime.datetime.fromtimestamp(creation_timestamp_2)
        formatted_time_2 = creation_datetime_2.strftime("%Y-%m-%d %H:%M:%S")

        md5_checksum = get_md5_hash(file)

        return round(os.path.getsize(file) / (1024*1024), 2), formatted_time_1, formatted_time_2, md5_checksum[-8:]





class MainWindow(QMainWindow):
    topic_template = "Всего файлов: {}    Сканировано файлов: {}    Просканированно: {:.2f} мб    Дубликатов найдено: {}"

    def __init__(self):
        super(MainWindow, self).__init__()

        self.DFF = DuplicateFileFinder()
        self.progress_text = ""

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.path_lineEdit.setText(os.path.abspath(os.curdir))
        self.ui.pathEdit_pushButton.clicked.connect(self.set_path)
        self.ui.scan_pushButton.clicked.connect(self.scan)
        # self.ui.moveToTrash_pushButton.clicked.connect(self.test)

        self.ui.topic_label.setText(self.topic_template.format(0, 0, 0, 0))

    def insert_progress(self, text, detailed, progress):
        QCoreApplication.processEvents()
        if not detailed or self.ui.detailProgress_checkBox.isChecked():
            self.progress_text += text + "\n"
            self.ui.progress_textEdit.setText(self.progress_text)

            for i in range(2):  # range(3) or range(4), range(2) works for me
                self.ui.progress_textEdit.update()
                cur_max = self.ui.progress_textEdit.verticalScrollBar().maximum()
                self.ui.progress_textEdit.verticalScrollBar().setValue(cur_max)

            self.ui.topic_label.setText(
                self.topic_template.format(progress.total_files, progress.files_scanned, progress.megabytes_scanned, progress.duples_found))

            if progress.total_files:
                self.ui.progressBar.setValue(round(progress.files_scanned / progress.total_files * 100, 1))
                if progress.megabytes_to_scan:
                    self.ui.progressBar_2.setValue(round(progress.megabytes_scanned / progress.megabytes_to_scan * 100, 1))

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

        duplicates = self.DFF.find_duplicates(self.ui.path_lineEdit.text(), lambda t, d, p: self.insert_progress(t, d, p))

        for dubs in duplicates:
            self.ui.verticalLayout_5.addWidget(DuplicateWidget(dubs, self))

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
