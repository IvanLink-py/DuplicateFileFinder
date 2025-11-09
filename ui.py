# -*- coding: utf-8 -*-
import sys
import os
import ctypes
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QTableWidgetItem, QFileDialog
from PySide6.QtCore import QRect, QCoreApplication
from PySide6.QtGui import QIcon
from dff import DuplicateFileFinder

from design.ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.DFF = DuplicateFileFinder()
        self.progress_text = ""

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.path_lineEdit.setText(os.path.abspath(os.curdir))
        self.ui.pathEdit_pushButton.clicked.connect(self.set_path)
        self.ui.scan_pushButton.clicked.connect(self.scan)



    def insert_progress(self, text, detailed):
        QCoreApplication.processEvents()
        if not detailed or self.ui.detailProgress_checkBox.isChecked():
            self.progress_text += text + "\n"
            self.ui.progress_textEdit.setText(self.progress_text)

            for i in range(2):  # range(3) or range(4), range(2) works for me
                self.ui.progress_textEdit.update()
                cur_max = self.ui.progress_textEdit.verticalScrollBar().maximum()
                self.ui.progress_textEdit.verticalScrollBar().setValue(cur_max)

    def set_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "Выберете путь", self.ui.path_lineEdit.text())
        if new_path is not None and new_path:
            self.ui.path_lineEdit.setText(new_path)

    def scan(self):
        self.ui.progressBar.setValue(0)
        self.progress_text = ""
        print(self.DFF.find_duplicates(self.ui.path_lineEdit.text(), lambda t, d: self.insert_progress(t, d)))
        self.ui.progressBar.setValue(100)



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
