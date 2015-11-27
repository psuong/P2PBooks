# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\Ui_ConfirmPurchaseDialog.ui'
#
# Created: Thu Nov 26 21:20:03 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(318, 562)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.cover_img_web_view = QtWebKit.QWebView(Dialog)
        self.cover_img_web_view.setUrl(QtCore.QUrl("about:blank"))
        self.cover_img_web_view.setObjectName("cover_img_web_view")
        self.gridLayout.addWidget(self.cover_img_web_view, 0, 0, 1, 2)
        self.summary_text_browser = QtGui.QTextBrowser(Dialog)
        self.summary_text_browser.setObjectName("summary_text_browser")
        self.gridLayout.addWidget(self.summary_text_browser, 1, 0, 1, 2)
        self.cost_label = QtGui.QLabel(Dialog)
        self.cost_label.setText("")
        self.cost_label.setObjectName("cost_label")
        self.gridLayout.addWidget(self.cost_label, 3, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.length_spin_box = QtGui.QSpinBox(Dialog)
        self.length_spin_box.setMinimum(1)
        self.length_spin_box.setMaximum(200)
        self.length_spin_box.setObjectName("length_spin_box")
        self.gridLayout.addWidget(self.length_spin_box, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.num_of_purchases_label = QtGui.QLabel(Dialog)
        self.num_of_purchases_label.setText("")
        self.num_of_purchases_label.setObjectName("num_of_purchases_label")
        self.gridLayout.addWidget(self.num_of_purchases_label, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Confirm Purchase", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Cost (per min)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Length (in minutes)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "# of Purchases", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
