# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\Ui_ReaderForm.ui'
#
# Created: Sat Oct 31 00:02:42 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(498, 543)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.published_by_line_edit = QtGui.QLineEdit(Form)
        self.published_by_line_edit.setObjectName("published_by_line_edit")
        self.gridLayout.addWidget(self.published_by_line_edit, 2, 1, 1, 1)
        self.ratings_line_edit = QtGui.QLineEdit(Form)
        self.ratings_line_edit.setObjectName("ratings_line_edit")
        self.gridLayout.addWidget(self.ratings_line_edit, 1, 1, 1, 1)
        self.title_line_edit = QtGui.QLineEdit(Form)
        self.title_line_edit.setObjectName("title_line_edit")
        self.gridLayout.addWidget(self.title_line_edit, 0, 1, 1, 1)
        self.report_push_button = QtGui.QPushButton(Form)
        self.report_push_button.setObjectName("report_push_button")
        self.gridLayout.addWidget(self.report_push_button, 3, 2, 1, 1)
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 4, 0, 1, 3)
        self.share_push_button = QtGui.QPushButton(Form)
        self.share_push_button.setObjectName("share_push_button")
        self.gridLayout.addWidget(self.share_push_button, 2, 2, 1, 1)
        self.read_pause_push_button = QtGui.QPushButton(Form)
        self.read_pause_push_button.setObjectName("read_pause_push_button")
        self.gridLayout.addWidget(self.read_pause_push_button, 3, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Reader", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Published by", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Ratings", None, QtGui.QApplication.UnicodeUTF8))
        self.report_push_button.setText(QtGui.QApplication.translate("Form", "Report", None, QtGui.QApplication.UnicodeUTF8))
        self.share_push_button.setText(QtGui.QApplication.translate("Form", "Share", None, QtGui.QApplication.UnicodeUTF8))
        self.read_pause_push_button.setText(QtGui.QApplication.translate("Form", "Read/Pause", None, QtGui.QApplication.UnicodeUTF8))

