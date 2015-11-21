# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\Ui_ConfirmPurchaseDialog.ui'
#
# Created: Sat Nov 21 17:25:01 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(356, 448)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.cover_img_web_view = QtWebKit.QWebView(Dialog)
        self.cover_img_web_view.setUrl(QtCore.QUrl("about:blank"))
        self.cover_img_web_view.setObjectName("cover_img_web_view")
        self.gridLayout.addWidget(self.cover_img_web_view, 0, 0, 1, 2)
        self.cost_label = QtGui.QLabel(Dialog)
        self.cost_label.setText("")
        self.cost_label.setObjectName("cost_label")
        self.gridLayout.addWidget(self.cost_label, 2, 1, 1, 1)
        self.summary_text_browser = QtGui.QTextBrowser(Dialog)
        self.summary_text_browser.setObjectName("summary_text_browser")
        self.gridLayout.addWidget(self.summary_text_browser, 1, 0, 1, 2)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.spinBox = QtGui.QSpinBox(Dialog)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(200)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Confirm Purchase", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Cost (per min):", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Length (in minutes)", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
