# -*- coding: utf-8 -*-
import ctypes
import os
import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from design.ui_MainWindow import Ui_MainWindow
from dff import DuplicateFileFinder


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
                self.topic_template.format(progress.total_files, progress.files_scanned, progress.megabytes_scanned, 0))

            if progress.total_files:
                self.ui.progressBar.setValue(round(progress.files_scanned / progress.total_files * 100, 1))
                if progress.megabytes_to_scan:
                    self.ui.progressBar_2.setValue(round(progress.megabytes_scanned / progress.megabytes_to_scan * 100, 1))

    def set_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Выберете путь", self.ui.path_lineEdit.text())
        if new_path is not None and new_path:
            self.ui.path_lineEdit.setText(new_path)

    def scan(self):
        self.ui.scan_pushButton.setEnabled(False)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar_2.setValue(0)
        self.progress_text = ""

        print(self.DFF.find_duplicates(self.ui.path_lineEdit.text(), lambda t, d, p: self.insert_progress(t, d, p)))

        self.ui.progressBar.setValue(100)
        self.ui.progressBar_2.setValue(100)
        self.ui.scan_pushButton.setEnabled(True)


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
