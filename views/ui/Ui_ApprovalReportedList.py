# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\Ui_ApprovalReportedList.ui'
#
# Created: Thu Nov 26 21:48:55 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(744, 429)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.approvals_table_widget = QtGui.QTableWidget(Form)
        self.approvals_table_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.approvals_table_widget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.approvals_table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.approvals_table_widget.setObjectName("approvals_table_widget")
        self.approvals_table_widget.setColumnCount(3)
        self.approvals_table_widget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.approvals_table_widget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.approvals_table_widget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.approvals_table_widget.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.approvals_table_widget, 1, 0, 1, 2)
        self.reports_table_widget = QtGui.QTableWidget(Form)
        self.reports_table_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.reports_table_widget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.reports_table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.reports_table_widget.setObjectName("reports_table_widget")
        self.reports_table_widget.setColumnCount(3)
        self.reports_table_widget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.reports_table_widget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.reports_table_widget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.reports_table_widget.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.reports_table_widget, 1, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.verify_reports_push_button = QtGui.QPushButton(Form)
        self.verify_reports_push_button.setObjectName("verify_reports_push_button")
        self.gridLayout.addWidget(self.verify_reports_push_button, 3, 3, 1, 1)
        self.verify_approval_push_button = QtGui.QPushButton(Form)
        self.verify_approval_push_button.setObjectName("verify_approval_push_button")
        self.gridLayout.addWidget(self.verify_approval_push_button, 3, 1, 1, 1)
        self.cancel_push_button = QtGui.QPushButton(Form)
        self.cancel_push_button.setObjectName("cancel_push_button")
        self.gridLayout.addWidget(self.cancel_push_button, 5, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 4)
        self.label = QtGui.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "P2PBooks", None, QtGui.QApplication.UnicodeUTF8))
        self.approvals_table_widget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "ISBN", None, QtGui.QApplication.UnicodeUTF8))
        self.approvals_table_widget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "Uploader", None, QtGui.QApplication.UnicodeUTF8))
        self.approvals_table_widget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "Asking Reward", None, QtGui.QApplication.UnicodeUTF8))
        self.reports_table_widget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "ISBN", None, QtGui.QApplication.UnicodeUTF8))
        self.reports_table_widget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "Report Reason", None, QtGui.QApplication.UnicodeUTF8))
        self.reports_table_widget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "Reporter", None, QtGui.QApplication.UnicodeUTF8))
        self.verify_reports_push_button.setText(QtGui.QApplication.translate("Form", "Verify", None, QtGui.QApplication.UnicodeUTF8))
        self.verify_approval_push_button.setText(QtGui.QApplication.translate("Form", "Verify", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_push_button.setText(QtGui.QApplication.translate("Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Awaiting Approval", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Reports", None, QtGui.QApplication.UnicodeUTF8))

