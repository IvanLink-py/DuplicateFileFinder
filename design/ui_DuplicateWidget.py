# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DuplicateWidgeteTXJko.ui'
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
    QLabel, QLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(564, 100)
        self.horizontalLayout_2 = QHBoxLayout(Frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(Frame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.path_label = QLabel(self.frame)
        self.path_label.setObjectName(u"path_label")
        self.path_label.setStyleSheet(u"font: 600 11pt \"Segoe UI\";")

        self.verticalLayout.addWidget(self.path_label)

        self.detail_label = QLabel(self.frame)
        self.detail_label.setObjectName(u"detail_label")

        self.verticalLayout.addWidget(self.detail_label)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(500, 6))
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.path_label_2 = QLabel(self.frame)
        self.path_label_2.setObjectName(u"path_label_2")
        self.path_label_2.setStyleSheet(u"font: 600 11pt \"Segoe UI\";")

        self.verticalLayout.addWidget(self.path_label_2)

        self.detail_label_2 = QLabel(self.frame)
        self.detail_label_2.setObjectName(u"detail_label_2")

        self.verticalLayout.addWidget(self.detail_label_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer = QSpacerItem(17, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMaximumSize(QSize(18, 16777215))

        self.verticalLayout_2.addWidget(self.checkBox)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_2.addWidget(self.frame)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.path_label.setText(QCoreApplication.translate("Frame", u"TextLabel", None))
        self.detail_label.setText(QCoreApplication.translate("Frame", u"TextLabel", None))
        self.path_label_2.setText(QCoreApplication.translate("Frame", u"TextLabel", None))
        self.detail_label_2.setText(QCoreApplication.translate("Frame", u"TextLabel", None))
    # retranslateUi

