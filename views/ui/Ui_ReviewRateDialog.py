# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/Ui_ReviewRateDialog.ui'
#
# Created: Thu Nov 26 21:19:02 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.review_text_edit = QtGui.QTextEdit(Dialog)
        self.review_text_edit.setObjectName("review_text_edit")
        self.gridLayout.addWidget(self.review_text_edit, 3, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.rating_combo_box = QtGui.QComboBox(Dialog)
        self.rating_combo_box.setObjectName("rating_combo_box")
        self.gridLayout.addWidget(self.rating_combo_box, 1, 0, 1, 1)
        self.submit_push_button = QtGui.QPushButton(Dialog)
        self.submit_push_button.setObjectName("submit_push_button")
        self.gridLayout.addWidget(self.submit_push_button, 4, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Rating:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Review:", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_push_button.setText(QtGui.QApplication.translate("Dialog", "Submit", None, QtGui.QApplication.UnicodeUTF8))

