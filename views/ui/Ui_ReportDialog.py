# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_ReportDialog.ui'
#
# Created: Fri Oct 30 18:12:08 2015
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
        self.report_label = QtGui.QLabel(Dialog)
        self.report_label.setObjectName("report_label")
        self.gridLayout.addWidget(self.report_label, 0, 0, 1, 1)
        self.report_combo_box = QtGui.QComboBox(Dialog)
        self.report_combo_box.setObjectName("report_combo_box")
        self.gridLayout.addWidget(self.report_combo_box, 1, 0, 1, 1)
        self.report_text_edit = QtGui.QTextEdit(Dialog)
        self.report_text_edit.setObjectName("report_text_edit")
        self.gridLayout.addWidget(self.report_text_edit, 2, 0, 1, 1)
        self.report_button_box = QtGui.QDialogButtonBox(Dialog)
        self.report_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.report_button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.report_button_box.setObjectName("report_button_box")
        self.gridLayout.addWidget(self.report_button_box, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.report_button_box, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.report_button_box, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.report_label.setText(QtGui.QApplication.translate("Dialog", "Report user for reason:", None, QtGui.QApplication.UnicodeUTF8))

