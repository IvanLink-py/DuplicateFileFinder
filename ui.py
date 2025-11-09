# -*- coding: utf-8 -*-
import sys
import ctypes
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QTableWidgetItem
from PySide6.QtCore import QRect, QCoreApplication
from PySide6.QtGui import QIcon

from design.ui_MainWindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)




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
