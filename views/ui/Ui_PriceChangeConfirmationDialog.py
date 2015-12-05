# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer\Ui_PriceChangeConfirmationDialog.ui'
#
# Created: Fri Dec 04 20:47:24 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 206)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.book_label = QtGui.QLabel(Dialog)
        self.book_label.setText("")
        self.book_label.setObjectName("book_label")
        self.gridLayout.addWidget(self.book_label, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.textBrowser = QtGui.QTextBrowser(Dialog)
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 2)
        self.su_price_label = QtGui.QLabel(Dialog)
        self.su_price_label.setText("")
        self.su_price_label.setObjectName("su_price_label")
        self.gridLayout.addWidget(self.su_price_label, 4, 1, 1, 1)
        self.asking_price_label = QtGui.QLabel(Dialog)
        self.asking_price_label.setText("")
        self.asking_price_label.setObjectName("asking_price_label")
        self.gridLayout.addWidget(self.asking_price_label, 3, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.No|QtGui.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "EBook Price Confirmation", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "ISBN", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Asking price", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "SU price", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You have recently submitted a book for approval, however, the SU has decided to award less than the asking price. Click Yes to accept the new price or click No to delete your original upload. No points will be altered if No is clicked but the EBook will not show up in the catalogue.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

