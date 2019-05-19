# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vision.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(587, 339)
        self.load_image = QtWidgets.QPushButton(Form)
        self.load_image.setGeometry(QtCore.QRect(0, 310, 75, 23))
        self.load_image.setObjectName("load_image")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(9, 19, 531, 251))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 529, 249))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(10, 0, 501, 251))
        self.label.setText("")
        self.label.setObjectName("label")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.load_image.setText(_translate("Form", "load_image"))

