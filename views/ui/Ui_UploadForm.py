# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/Ui_UploadForm.ui'
#
# Created: Sat Nov 21 21:07:37 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(531, 576)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(9, 9, 20, 16))
        self.label_2.setObjectName("label_2")
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(271, 9, 33, 16))
        self.label.setObjectName("label")
        self.author_line_edit = QtGui.QLineEdit(Form)
        self.author_line_edit.setGeometry(QtCore.QRect(271, 28, 251, 20))
        self.author_line_edit.setObjectName("author_line_edit")
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(9, 54, 34, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(271, 54, 34, 16))
        self.label_4.setObjectName("label_4")
        self.genres_combo_box = QtGui.QComboBox(Form)
        self.genres_combo_box.setGeometry(QtCore.QRect(9, 73, 251, 20))
        self.genres_combo_box.setObjectName("genres_combo_box")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.genres_combo_box.addItem("")
        self.isbn_line_edit = QtGui.QLineEdit(Form)
        self.isbn_line_edit.setGeometry(QtCore.QRect(271, 73, 251, 20))
        self.isbn_line_edit.setObjectName("isbn_line_edit")
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(9, 105, 23, 16))
        self.label_5.setObjectName("label_5")
        self.price_spin_box = QtGui.QSpinBox(Form)
        self.price_spin_box.setGeometry(QtCore.QRect(9, 124, 251, 20))
        self.price_spin_box.setMaximum(9999)
        self.price_spin_box.setObjectName("price_spin_box")
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(370, 130, 61, 16))
        self.label_7.setObjectName("label_7")
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 160, 44, 16))
        self.label_6.setObjectName("label_6")
        self.pick_image_push_button = QtGui.QPushButton(Form)
        self.pick_image_push_button.setGeometry(QtCore.QRect(370, 150, 75, 23))
        self.pick_image_push_button.setObjectName("pick_image_push_button")
        self.summary_plain_text_edit = QtGui.QPlainTextEdit(Form)
        self.summary_plain_text_edit.setGeometry(QtCore.QRect(9, 179, 256, 271))
        self.summary_plain_text_edit.setObjectName("summary_plain_text_edit")
        self.cover_img_web_view = QtWebKit.QWebView(Form)
        self.cover_img_web_view.setGeometry(QtCore.QRect(271, 179, 251, 324))
        self.cover_img_web_view.setMinimumSize(QtCore.QSize(200, 300))
        self.cover_img_web_view.setMaximumSize(QtCore.QSize(300, 350))
        self.cover_img_web_view.setUrl(QtCore.QUrl("about:blank"))
        self.cover_img_web_view.setObjectName("cover_img_web_view")
        self.upload_push_button = QtGui.QPushButton(Form)
        self.upload_push_button.setGeometry(QtCore.QRect(10, 480, 251, 23))
        self.upload_push_button.setObjectName("upload_push_button")
        self.file_location_label = QtGui.QLabel(Form)
        self.file_location_label.setGeometry(QtCore.QRect(10, 510, 511, 16))
        self.file_location_label.setWordWrap(True)
        self.file_location_label.setObjectName("file_location_label")
        self.submit_push_button = QtGui.QPushButton(Form)
        self.submit_push_button.setGeometry(QtCore.QRect(10, 540, 511, 23))
        self.submit_push_button.setObjectName("submit_push_button")
        self.title_line_edit = QtGui.QLineEdit(Form)
        self.title_line_edit.setGeometry(QtCore.QRect(9, 28, 251, 20))
        self.title_line_edit.setObjectName("title_line_edit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Author", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Genres", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "ISBN #", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(0, QtGui.QApplication.translate("Form", "Kids", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(1, QtGui.QApplication.translate("Form", "Adventure", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(2, QtGui.QApplication.translate("Form", "Education", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(3, QtGui.QApplication.translate("Form", "DIY", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(4, QtGui.QApplication.translate("Form", "Romance", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(5, QtGui.QApplication.translate("Form", "Comedy", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(6, QtGui.QApplication.translate("Form", "Fantasy", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(7, QtGui.QApplication.translate("Form", "Biography", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(8, QtGui.QApplication.translate("Form", "History", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(9, QtGui.QApplication.translate("Form", "Magazine", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(10, QtGui.QApplication.translate("Form", "Religion", None, QtGui.QApplication.UnicodeUTF8))
        self.genres_combo_box.setItemText(11, QtGui.QApplication.translate("Form", "Sports", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Price", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Cover Image", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Form", "Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.pick_image_push_button.setText(QtGui.QApplication.translate("Form", "Pick Image", None, QtGui.QApplication.UnicodeUTF8))
        self.upload_push_button.setText(QtGui.QApplication.translate("Form", "Select PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.file_location_label.setText(QtGui.QApplication.translate("Form", "File:", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_push_button.setText(QtGui.QApplication.translate("Form", "Submit", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
