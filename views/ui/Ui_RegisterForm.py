# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\Ui_RegisterForm.ui'
#
# Created: Fri Nov 06 22:05:31 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(444, 171)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 1)
        self.submit_push_button = QtGui.QPushButton(Form)
        self.submit_push_button.setObjectName("submit_push_button")
        self.gridLayout.addWidget(self.submit_push_button, 10, 3, 1, 1)
        self.username_line_edit = QtGui.QLineEdit(Form)
        self.username_line_edit.setObjectName("username_line_edit")
        self.gridLayout.addWidget(self.username_line_edit, 1, 2, 1, 2)
        self.password_line_edit = QtGui.QLineEdit(Form)
        self.password_line_edit.setObjectName("password_line_edit")
        self.gridLayout.addWidget(self.password_line_edit, 4, 2, 1, 2)
        self.confirm_password_line_edit = QtGui.QLineEdit(Form)
        self.confirm_password_line_edit.setObjectName("confirm_password_line_edit")
        self.gridLayout.addWidget(self.confirm_password_line_edit, 6, 2, 1, 2)
        self.email_line_edit = QtGui.QLineEdit(Form)
        self.email_line_edit.setObjectName("email_line_edit")
        self.gridLayout.addWidget(self.email_line_edit, 7, 2, 1, 2)
        self.dob_date_edit = QtGui.QDateEdit(Form)
        self.dob_date_edit.setObjectName("dob_date_edit")
        self.gridLayout.addWidget(self.dob_date_edit, 9, 2, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.username_line_edit, self.password_line_edit)
        Form.setTabOrder(self.password_line_edit, self.confirm_password_line_edit)
        Form.setTabOrder(self.confirm_password_line_edit, self.email_line_edit)
        Form.setTabOrder(self.email_line_edit, self.dob_date_edit)
        Form.setTabOrder(self.dob_date_edit, self.submit_push_button)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Confirm Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Email", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "DOB", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_push_button.setText(QtGui.QApplication.translate("Form", "Submit", None, QtGui.QApplication.UnicodeUTF8))

