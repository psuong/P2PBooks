# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/Ui_ReviewRateDialog.ui'
#
# Created: Thu Nov 26 21:09:01 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Review_Rate(object):
    def setupUi(self, Review_Rate):
        Review_Rate.setObjectName("Review_Rate")
        Review_Rate.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Review_Rate)
        self.gridLayout.setObjectName("gridLayout")
        self.review_text_edit = QtGui.QTextEdit(Review_Rate)
        self.review_text_edit.setObjectName("review_text_edit")
        self.gridLayout.addWidget(self.review_text_edit, 3, 0, 1, 1)
        self.label = QtGui.QLabel(Review_Rate)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.rating_combo_box = QtGui.QComboBox(Review_Rate)
        self.rating_combo_box.setObjectName("rating_combo_box")
        self.gridLayout.addWidget(self.rating_combo_box, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Review_Rate)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.retranslateUi(Review_Rate)
        QtCore.QMetaObject.connectSlotsByName(Review_Rate)

    def retranslateUi(self, Review_Rate):
        Review_Rate.setWindowTitle(QtGui.QApplication.translate("Review_Rate", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Review_Rate", "Rating:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Review_Rate", "Review:", None, QtGui.QApplication.UnicodeUTF8))

