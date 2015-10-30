# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/Ui_LoginForm.ui'
#
# Created: Fri Oct 30 15:36:23 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(377, 205)
        self.formLayout = QtGui.QFormLayout(Form)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.user_name_label = QtGui.QLabel(Form)
        self.user_name_label.setObjectName("user_name_label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.user_name_label)
        self.username_line_edit = QtGui.QLineEdit(Form)
        self.username_line_edit.setObjectName("username_line_edit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.username_line_edit)
        self.password_label = QtGui.QLabel(Form)
        self.password_label.setObjectName("password_label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.password_label)
        self.password_line_edit = QtGui.QLineEdit(Form)
        self.password_line_edit.setObjectName("password_line_edit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.password_line_edit)
        self.sign_up_push_button = QtGui.QPushButton(Form)
        self.sign_up_push_button.setObjectName("sign_up_push_button")
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.sign_up_push_button)
        self.login_push_button = QtGui.QPushButton(Form)
        self.login_push_button.setObjectName("login_push_button")
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.login_push_button)
        self.guest_session_push_button = QtGui.QPushButton(Form)
        self.guest_session_push_button.setObjectName("guest_session_push_button")
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.guest_session_push_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Login Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.user_name_label.setText(QtGui.QApplication.translate("Form", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.password_label.setText(QtGui.QApplication.translate("Form", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.sign_up_push_button.setText(QtGui.QApplication.translate("Form", "Sign Up", None, QtGui.QApplication.UnicodeUTF8))
        self.login_push_button.setText(QtGui.QApplication.translate("Form", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.guest_session_push_button.setText(QtGui.QApplication.translate("Form", "Guest Session", None, QtGui.QApplication.UnicodeUTF8))

