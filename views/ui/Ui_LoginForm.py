# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\Ui_LoginForm.ui'
#
# Created: Fri Nov 27 18:44:18 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(377, 140)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.user_name_label = QtGui.QLabel(Form)
        self.user_name_label.setObjectName("user_name_label")
        self.gridLayout.addWidget(self.user_name_label, 0, 0, 1, 1)
        self.username_line_edit = QtGui.QLineEdit(Form)
        self.username_line_edit.setObjectName("username_line_edit")
        self.gridLayout.addWidget(self.username_line_edit, 0, 1, 1, 1)
        self.password_label = QtGui.QLabel(Form)
        self.password_label.setObjectName("password_label")
        self.gridLayout.addWidget(self.password_label, 1, 0, 1, 1)
        self.password_line_edit = QtGui.QLineEdit(Form)
        self.password_line_edit.setObjectName("password_line_edit")
        self.gridLayout.addWidget(self.password_line_edit, 1, 1, 1, 1)
        self.login_push_button = QtGui.QPushButton(Form)
        self.login_push_button.setObjectName("login_push_button")
        self.gridLayout.addWidget(self.login_push_button, 2, 0, 1, 2)
        self.sign_up_push_button = QtGui.QPushButton(Form)
        self.sign_up_push_button.setObjectName("sign_up_push_button")
        self.gridLayout.addWidget(self.sign_up_push_button, 3, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Login Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.user_name_label.setText(QtGui.QApplication.translate("Form", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.password_label.setText(QtGui.QApplication.translate("Form", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.login_push_button.setText(QtGui.QApplication.translate("Form", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.sign_up_push_button.setText(QtGui.QApplication.translate("Form", "Sign Up", None, QtGui.QApplication.UnicodeUTF8))

