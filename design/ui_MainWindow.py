# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindowKYGWRo.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(894, 544)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 600 12pt \"Segoe UI\";")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.path_lineEdit = QLineEdit(self.centralwidget)
        self.path_lineEdit.setObjectName(u"path_lineEdit")

        self.horizontalLayout.addWidget(self.path_lineEdit)

        self.pathEdit_pushButton = QPushButton(self.centralwidget)
        self.pathEdit_pushButton.setObjectName(u"pathEdit_pushButton")
        self.pathEdit_pushButton.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.pathEdit_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.skipSystem_checkBox = QCheckBox(self.centralwidget)
        self.skipSystem_checkBox.setObjectName(u"skipSystem_checkBox")

        self.horizontalLayout_2.addWidget(self.skipSystem_checkBox)

        self.skipCache_checkBox = QCheckBox(self.centralwidget)
        self.skipCache_checkBox.setObjectName(u"skipCache_checkBox")

        self.horizontalLayout_2.addWidget(self.skipCache_checkBox)

        self.skipGit_checkBox = QCheckBox(self.centralwidget)
        self.skipGit_checkBox.setObjectName(u"skipGit_checkBox")

        self.horizontalLayout_2.addWidget(self.skipGit_checkBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.detailProgress_checkBox = QCheckBox(self.centralwidget)
        self.detailProgress_checkBox.setObjectName(u"detailProgress_checkBox")

        self.horizontalLayout_2.addWidget(self.detailProgress_checkBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))
        self.label_2.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_4.addWidget(self.label_2)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.horizontalLayout_4.addWidget(self.progressBar)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))
        self.label_3.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_5.addWidget(self.label_3)

        self.progressBar_2 = QProgressBar(self.centralwidget)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(0)

        self.horizontalLayout_5.addWidget(self.progressBar_2)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.topic_label = QLabel(self.centralwidget)
        self.topic_label.setObjectName(u"topic_label")

        self.verticalLayout.addWidget(self.topic_label)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.progress_textEdit = QTextEdit(self.tab)
        self.progress_textEdit.setObjectName(u"progress_textEdit")
        self.progress_textEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.progress_textEdit)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(self.tab_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 850, 220))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scan_pushButton = QPushButton(self.centralwidget)
        self.scan_pushButton.setObjectName(u"scan_pushButton")
        self.scan_pushButton.setStyleSheet(u"background-color: rgb(30, 77, 23);\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_3.addWidget(self.scan_pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.delete_pushButton = QPushButton(self.centralwidget)
        self.delete_pushButton.setObjectName(u"delete_pushButton")
        self.delete_pushButton.setStyleSheet(u"background-color: rgb(77, 23, 23);\n"
"color: rgb(255, 255, 255);")

        self.horizontalLayout_3.addWidget(self.delete_pushButton)

        self.moveToTrash_pushButton = QPushButton(self.centralwidget)
        self.moveToTrash_pushButton.setObjectName(u"moveToTrash_pushButton")

        self.horizontalLayout_3.addWidget(self.moveToTrash_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 894, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"DFF", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a \u0438 \u0443\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0434\u0443\u0431\u043b\u0438\u043a\u0430\u0442\u043e\u0432 \u0444\u0430\u0439\u043b\u043e\u0432", None))
        self.path_lineEdit.setPlaceholderText("")
        self.pathEdit_pushButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.skipSystem_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u0441\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0435 \u0444\u0430\u0439\u043b\u044b", None))
        self.skipCache_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u043a\u044d\u0448 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u043e\u0432", None))
        self.skipGit_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c .git", None))
        self.detailProgress_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u044b\u0439 \u043f\u0440\u043e\u0433\u0440\u0435\u0441\u0441", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0411\u044b\u0441\u0442\u0440\u043e\u0435 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0435\u0442\u0430\u043b\u044c\u043d\u043e\u0435 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
        self.topic_label.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0433\u0440\u0435\u0441\u0441", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442", None))
        self.scan_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.delete_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c (\u0431\u0435\u0437\u0432\u043e\u0437\u0432\u0440\u0430\u0442\u043d\u043e)", None))
        self.moveToTrash_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u043c\u0435\u0441\u0442\u0438\u0442\u044c \u0432 \u043a\u0430\u0440\u0437\u0438\u043d\u0443", None))
    # retranslateUi

