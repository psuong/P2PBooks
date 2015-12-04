# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\Ui_ShareRequestWidget.ui'
#
# Created: Thu Dec 03 19:07:46 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(529, 294)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.accept_push_button = QtGui.QPushButton(Form)
        self.accept_push_button.setObjectName("accept_push_button")
        self.gridLayout.addWidget(self.accept_push_button, 2, 1, 1, 1)
        self.decline_push_button = QtGui.QPushButton(Form)
        self.decline_push_button.setObjectName("decline_push_button")
        self.gridLayout.addWidget(self.decline_push_button, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.share_request_table_widget = QtGui.QTableWidget(Form)
        self.share_request_table_widget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.share_request_table_widget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.share_request_table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.share_request_table_widget.setObjectName("share_request_table_widget")
        self.share_request_table_widget.setColumnCount(9)
        self.share_request_table_widget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.share_request_table_widget.setHorizontalHeaderItem(8, item)
        self.gridLayout.addWidget(self.share_request_table_widget, 1, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "P2PBooks", None, QtGui.QApplication.UnicodeUTF8))
        self.accept_push_button.setText(QtGui.QApplication.translate("Form", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.decline_push_button.setText(QtGui.QApplication.translate("Form", "Decline", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "ISBN", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Form", "Cost", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("Form", "Uploader", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("Form", "Rating", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("Form", "Time Requested", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(7).setText(QtGui.QApplication.translate("Form", "Total Cost", None, QtGui.QApplication.UnicodeUTF8))
        self.share_request_table_widget.horizontalHeaderItem(8).setText(QtGui.QApplication.translate("Form", "Sharer", None, QtGui.QApplication.UnicodeUTF8))

