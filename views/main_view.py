from PySide import QtGui, QtCore
from ui import Ui_UploadForm, Ui_ReaderForm, Ui_ReportDialog, Ui_LoginForm, Ui_RegisterForm, Ui_MainWindowVisitor, \
    Ui_MainWindowRegistered, Ui_ConfirmPurchaseDialog, Ui_ApprovalReportedList, Ui_BadWordsDialog, Ui_ReviewRateDialog
from models.main_model import submit_upload_form, submit_report_form, submit_review_rate_form
from database.database_objects import load_serialized_user, load_serialized_ebook, PurchasedEBook, serialize_user,\
    update_serialized_ebook
import os
import datetime
import sys

# Change default encoding to be utf-8 for searching bad words in book_text
reload(sys)
sys.setdefaultencoding('utf8')


class UploadFormView(QtGui.QWidget):
    def __init__(self, model, username, main_window_inst):
        self.model = model
        super(UploadFormView, self).__init__()
        self.ui = Ui_UploadForm.Ui_Form()
        self.build_ui()
        self.file_location = None
        self.new_book_added = False
        self.cover_img_location = None
        self.main_window = main_window_inst
        self.username = username

    def build_ui(self):
        self.ui.setupUi(self)
        # Disable text edit and also put a temporary message
        # self.ui.preview_text_edit.setText('Please click upload to show preview.')
        # self.ui.preview_text_edit.setDisabled(True)

        # Connect buttons to functions
        self.ui.upload_push_button.clicked.connect(self.upload)
        self.ui.pick_image_push_button.clicked.connect(self.pick_image)
        self.ui.submit_push_button.clicked.connect(self.submit)

    def upload(self):
        file_location = QtGui.QFileDialog.getOpenFileName(self, 'Open eBook', '', 'eBook Formats (*.pdf *.txt)')
        self.file_location = file_location[0]
        if self.file_location:
            self.ui.file_location_label.setText("File: " + self.file_location)

    def pick_image(self):
        file_location = QtGui.QFileDialog.getOpenFileName(self,
                                                          'Open cover image',
                                                          '',
                                                          'image formats (*.png *.jpg *jpeg)')
        self.cover_img_location = file_location[0]
        if self.cover_img_location:
            self.ui.cover_img_web_view.setHtml('<img alt="Cover img" '
                                               + 'src="' + self.cover_img_location
                                               + '" style="width: 225px; height: 325px">')

    def submit(self):
        # Make sure all fields are entered before submitting
        if self.ui.title_line_edit.text() and self.ui.author_line_edit.text() and self.ui.isbn_line_edit.text():
            does_file_exist = os.path.isfile(self.file_location)
            if does_file_exist:
                # File uploaded successfully
                submit_upload_form(self.ui.title_line_edit.text(),
                                   self.ui.author_line_edit.text(),
                                   self.ui.genres_combo_box.currentText(),
                                   self.ui.isbn_line_edit.text(),
                                   self.ui.price_spin_box.text(),
                                   self.username,
                                   self.ui.summary_plain_text_edit.toPlainText(),
                                   self.cover_img_location,
                                   self.file_location,
                                   )
                self.new_book_added = True
                self.close()
            else:
                # Returns an Error message if file DNE
                QtGui.QMessageBox.about(self, "Invalid PDF", "PDF file does not exist: " + str(self.file_location))
        else:
            QtGui.QMessageBox.about(self, "Error", "Fields must be filled in.")

    def closeEvent(self, *args, **kwargs):
        self.main_window.show()
        if self.new_book_added:
            self.main_window.load_ebooks()
        super(UploadFormView, self).hide()


class ConfirmedPurchaseDialogView(QtGui.QDialog):
    def __init__(self, model, username, rate, cover_img, summary, main_window_inst, isbn):
        self.model = model
        self.main_window = main_window_inst
        self.username = username
        self.rate = rate
        self.cover_img = cover_img
        self.summary = summary
        self.isbn = isbn
        super(ConfirmedPurchaseDialogView, self).__init__()
        self.ui = Ui_ConfirmPurchaseDialog.Ui_Dialog()
        self.build_ui()

        # Load the user info + book info
        self.user_instance = load_serialized_user(self.username)
        self.ebook_in_transaction = load_serialized_ebook(self.isbn)

    def build_ui(self):
        self.ui.setupUi(self)

        self.ui.summary_text_browser.setText(self.summary)
        self.ui.cover_img_web_view.setHtml('<img alt="Cover img" '
                                           'src="' + self.cover_img + '" style="width: 300px; height: 300px">')
        self.ui.cost_label.setText(str(self.rate))

    def accept(self, *args, **kwargs):
        if self.user_instance.credits >= self.ebook_in_transaction.price * self.ui.length_spin_box.value():
            if self.user_instance.rented_books[self.isbn]:
                self.user_instance.rented_books[self.isbn].length_on_rent += self.ui.length_spin_box.value()
            else:
                ebook_purchase = PurchasedEBook(self.username,
                                                self.isbn,
                                                datetime.datetime.now(),
                                                self.ui.length_spin_box.value(),
                                                datetime.datetime.now())

                self.user_instance.rented_books[self.isbn] = ebook_purchase

            self.user_instance.credits -= (self.ebook_in_transaction.price * self.ui.length_spin_box.value())
            serialize_user(self.user_instance, self.user_instance.__unicode__)
            self.main_window.reload_user_info()
            self.hide()
        else:
            # NOT ENOUGH FUNDS; THROW ERROR
            pass


class ReportDialogView(QtGui.QDialog):
    def __init__(self, model, book_instance, reporter, reason=""):
        self.model = model
        super(ReportDialogView, self).__init__()
        self.ui = Ui_ReportDialog.Ui_Dialog()
        self.reporter = reporter
        self.book_instance = book_instance
        self.bad_words_dialog = BadWordsDialogView(self.model, self.book_instance, self.reporter)
        self.build_ui(reason)

    def build_ui(self, reason):
        self.ui.setupUi(self)

        # Give reason options to report_combo_box
        self.ui.report_combo_box.addItems(["",
                                           "Violent/repulsive content",
                                           "Spam/misleading",
                                           "Copyright violation infringement",
                                           "None of the above (Specify below)",
                                           ])

        if reason != "":
            self.ui.report_text_edit.setText(reason)
            self.ui.report_combo_box.setCurrentIndex(1)

        # Opens bad_words_dialog on activate of index 1 ("Violent/repulsive content")
        self.connect(self.ui.report_combo_box, QtCore.SIGNAL("activated(int)"),
                     self.show_bad_words_dialog)

    def accept(self, *args, **kwargs):
        # Press OK
        report_selection = str(self.ui.report_combo_box.currentText())
        report_description = str(self.ui.report_text_edit.toPlainText())
        if report_selection != "":
            if report_selection == "None of the above (Specify below)" and report_description == "":
                # Display an error message to tell the user to write a description
                QtGui.QMessageBox.about(self, "Error", "Please specify the reason in the description")
            else:
                # Send the selection and description
                submit_report_form(self.reporter.username, report_selection, report_description, self.book_instance)
                self.close()
        else:
            # Display an error message to tell the user to select a selection from the combo box
            QtGui.QMessageBox.about(self, "Error", "Please select a reason from the dropdown")

    @QtCore.Slot()
    def show_bad_words_dialog(self, index):
        if index == 1:
            self.close()
            self.bad_words_dialog.show()


class BadWordsDialogView(QtGui.QDialog):
    def __init__(self, model, book_instance, reporter):
        self.model = model
        self.book_instance = book_instance
        super(BadWordsDialogView, self).__init__()
        self.reporter = reporter
        self.ui = Ui_BadWordsDialog.Ui_Dialog()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)
        self.ui.search_push_button.clicked.connect(self.search_words)

    @QtCore.Slot()
    def search_words(self):
        bad_words_text = self.ui.bad_words_text_edit.toPlainText()
        if bad_words_text == "":
            # Display an error message to tell the user to write a description
            QtGui.QMessageBox.about(self, "Error", "You have not yet listed any bad words")
        else:
            bad_words_list = bad_words_text.split(', ')
            book_text = self.book_instance.book_text
            reason = "Bad Words: \n"
            for word in bad_words_list:
                if book_text.find(word.lower(), 0, len(book_text)) >= 0:
                    reason += word + ": Found \n"
                else:
                    reason += word + ": Not Found \n"

            self.hide()
            self.report_dialog = ReportDialogView(self.model, self.book_instance, self.reporter, reason)
            self.report_dialog.show()


class ReaderFormView(QtGui.QWidget):
    def __init__(self, model, main_window, book_isbn, user_instance):
        self.model = model
        self.user_instance = user_instance
        self.main_window = main_window
        self.book_purchase_info = user_instance.rented_books[book_isbn]
        self.book_instance = load_serialized_ebook(book_isbn)
        super(ReaderFormView, self).__init__()
        self.ui = Ui_ReaderForm.Ui_Form()
        self.report_dialog = ReportDialogView(self.model, self.book_instance, self.user_instance)
        self.review_rate_dialog = ReviewRateDialogView(self.model, self.book_instance, self.user_instance)
        self.timer = QtCore.QTimer(self)
        self.paused = True
        self.pdf_reader_location = None
        self.reader_process = None
        self.build_ui()

        self.count_seconds = 0

    def build_ui(self):
        self.ui.setupUi(self)

        # Disable line edits
        self.ui.uploader_by_line_edit.setDisabled(True)
        self.ui.ratings_line_edit.setDisabled(True)
        self.ui.title_line_edit.setDisabled(True)

        self.ui.uploader_by_line_edit.setText(self.book_instance.uploader.username)
        self.ui.ratings_line_edit.setText(str(self.book_instance.rating))
        self.ui.title_line_edit.setText(self.book_instance.title)

        # Set book to paused state
        self.ui.read_pause_push_button.setText('Read')
        if self.user_instance.default_pdf_reader is not None:
            self.pdf_reader_location = self.user_instance.default_pdf_reader
            self.ui.pdf_reader_path_label.setText(self.user_instance.default_pdf_reader)

        self.ui.checkout_at_label.setText(self.book_purchase_info.checked_out_time.strftime('%H:%M:%S %m/%d/%y'))
        # Time remaining, lock read if 0
        self.ui.time_remaining_label.setText(str(self.book_purchase_info.length_on_rent) + ' seconds')
        if self.book_purchase_info.length_on_rent == 0:
            self.ui.read_pause_push_button.setDisabled(True)

        # Connect buttons
        self.ui.read_pause_push_button.clicked.connect(self.read_pause)
        self.ui.share_push_button.clicked.connect(self.share)
        self.ui.report_push_button.clicked.connect(self.report)
        self.ui.review_rate_push_button.clicked.connect(self.review_rate)
        self.ui.browse_pdf_reader_push_button.clicked.connect(self.browse_reader_location)

        self.timer.timeout.connect(self.show_time)

    @QtCore.Slot()
    def show_time(self):
        self.count_seconds += 1
        self.book_purchase_info.length_on_rent -= 1
        self.ui.time_remaining_label.setText(str(self.book_purchase_info.length_on_rent) + ' seconds')
        if self.book_purchase_info.length_on_rent == 0:
            self.reader_process.kill()
            self.timer.stop()
            self.ui.read_pause_push_button.setDisabled(True)

    @QtCore.Slot()
    def read_pause(self):
        if not self.paused:
            # Pause the book
            self.paused = True
            self.reader_process.kill()
            self.timer.stop()
            self.book_purchase_info.paused_time = datetime.datetime.now()
            self.book_instance.add_seconds(self.count_seconds)
            update_serialized_ebook(self.book_instance)
        else:
            self.count_seconds = 0
            # Check if book can be read
            arguments = [os.path.join('database', 'blobs', 'ebooks', self.book_instance.isbn + '.pdf')]
            self.reader_process = QtCore.QProcess(self)
            self.reader_process.started.connect(self.started)
            self.reader_process.finished.connect(self.finished)
            self.reader_process.start(self.pdf_reader_location, arguments)
            self.paused = False

    @QtCore.Slot()
    def started(self):
        self.ui.read_pause_push_button.setText('Pause')
        self.timer.start(1000)

    @QtCore.Slot()
    def finished(self):
        self.ui.read_pause_push_button.setText('Read')
        self.timer.stop()

    @QtCore.Slot()
    def share(self):
        # Trigger the share widget
        pass

    @QtCore.Slot()
    def report(self):
        # Trigger the report widget
        self.report_dialog.show()

    @QtCore.Slot()
    def review_rate(self):
        # Trigger the report widget
        self.review_rate_dialog.show()

    @QtCore.Slot()
    def browse_reader_location(self):
        pdf_reader = QtGui.QFileDialog.getOpenFileName(self, 'Open PDF Reader', '',
                                                       'PDF Reader Formats (*.exe)')
        if pdf_reader[1]:
            self.ui.pdf_reader_path_label.setText(pdf_reader[0])
            self.pdf_reader_location = pdf_reader[0]

    def closeEvent(self, *args, **kwargs):
        self.user_instance.default_pdf_reader = self.pdf_reader_location
        serialize_user(self.user_instance, self.user_instance.username)
        self.main_window.show()
        self.hide()


class ReviewRateDialogView(QtGui.QDialog):
    def __init__(self, model, book_instance, reviewer):
        self.model = model
        super(ReviewRateDialogView, self).__init__()
        self.ui = Ui_ReviewRateDialog.Ui_Dialog()

        self.book_instance = book_instance
        self.reviewer = reviewer

        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Setup combo box
        self.ui.rating_combo_box.addItems(["", "1", "2", "3", "4", "5"])

        self.ui.submit_push_button.clicked.connect(self.submit)

    @QtCore.Slot()
    def submit(self):
        review_text = self.ui.review_text_edit.toPlainText()
        if review_text == "":
            # Display an error message to tell the user to write a description
            QtGui.QMessageBox.about(self, "Error", "You have not yet written anything in the review")
        else:
            submit_review_rate_form(self.book_instance, self.reviewer, int(self.ui.rating_combo_box.currentText()),
                                    review_text)


class LoginFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(LoginFormView, self).__init__()
        self.ui = Ui_LoginForm.Ui_Form()
        self.build_ui()
        self.main_window = None
        self.register_window = None
        self.user_file = None

    def build_ui(self):
        self.ui.setupUi(self)
        # Connect buttons to their respective functions
        self.ui.login_push_button.clicked.connect(self.login)
        self.ui.sign_up_push_button.clicked.connect(self.sign_up)
        self.ui.password_line_edit.setEchoMode(QtGui.QLineEdit.EchoMode.Password)

    def login(self):
        # Grab component in object
        username = self.ui.username_line_edit.text()
        password = self.ui.password_line_edit.text()

        # Checks if the username and passwords are empty string
        if username == '' and password == '':
            QtGui.QMessageBox.about(self, "Error", "Invalid password and username.")
        # Checks if username is an empty string
        elif username == '' and password != '':
            QtGui.QMessageBox.about(self, "Error", "Invalid Username.")
        # Checks if password is an empty string
        elif password == '' and username != '':
            QtGui.QMessageBox.about(self, "Error", "Invalid Password.")
        else:
            # Check if the fields match a username and password is in the database
            if self.model.login_user(username, password) is not None:
                self.main_window = MainWindowRegisteredView(self.model, username)
                self.main_window.show()
                self.hide()
            else:
                # Nothing was return; error
                QtGui.QMessageBox.about(self, "Error", "No username/password found.")

    # sign_up(self) must open up the Register window
    def sign_up(self):
        self.register_window = RegisterFormView(self.model)
        self.register_window.show()
        self.hide()


class RegisterFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        self.registered_main_window = None
        super(RegisterFormView, self).__init__()
        self.ui = Ui_RegisterForm.Ui_Form()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)
        self.ui.password_line_edit.setEchoMode(QtGui.QLineEdit.EchoMode.Password)
        self.ui.confirm_password_line_edit.setEchoMode(QtGui.QLineEdit.EchoMode.Password)
        # Connect buttons to functions
        self.ui.submit_push_button.clicked.connect(self.submit)

    def submit(self):
        username = self.ui.username_line_edit.text()
        password = self.ui.password_line_edit.text()
        confirm_password = self.ui.confirm_password_line_edit.text()

        # Checks username and passwords
        if password == confirm_password and load_serialized_user(username) is None and username:
            self.model.register_user(username,
                                     password,
                                     self.ui.email_line_edit.text(),
                                     self.ui.dob_date_edit.date())
            self.registered_main_window = MainWindowRegisteredView(self.model,
                                                                   self.ui.username_line_edit.text())
            self.registered_main_window.show()
            self.hide()

        else:
            if load_serialized_user(username) is not None and password == confirm_password:
                QtGui.QMessageBox.about(self, "Invalid Username", "Username exists already")
            elif load_serialized_user(username) is None and password != confirm_password:
                QtGui.QMessageBox.about(self, "Incorrect Password Fields", "Password and Confirm Password "
                                                                           "are not the same!")
            elif load_serialized_user(username) is None and password != confirm_password:
                QtGui.QMessageBox.about(self, "Invalid Username & Password", "Username exists already and passwords"
                                                                             "do not match!")
            else:
                QtGui.QMessageBox.about(self, "Error", "Invalid Credentials")


class MainWindowVisitorView(QtGui.QMainWindow):
    def __init__(self, model):
        self.model = model
        self.purchase_dialog = None
        super(MainWindowVisitorView, self).__init__()
        self.ui = Ui_MainWindowVisitor.Ui_MainWindow()
        self.login_view = LoginFormView(self.model)
        self.register_view = RegisterFormView(self.model)
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Default text in Search Line Edit
        self.ui.search_line_edit.setPlaceholderText("Search...")

        # Hide results table widget for later
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()

        self.ui.go_push_button.clicked.connect(self.search)
        self.ui.close_push_button.clicked.connect(self.close_search)
        self.ui.search_line_edit.returnPressed.connect(self.search)
        self.ui.register_push_button.clicked.connect(self.register)
        self.ui.login_push_button.clicked.connect(self.login)

        # Connect checkout buttons
        self.ui.top_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.top_table_widget.selectedItems()))

        self.ui.kids_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.kids_table_widget.selectedItems()))

        self.ui.adventure_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.adventure_table_widget.selectedItems()))

        self.ui.edu_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.edu_table_widget.selectedItems()))

        self.ui.diy_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.diy_table_widget.selectedItems()))

        self.ui.romance_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.romance_table_widget.selectedItems()))

        self.ui.comedy_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.comedy_table_widget.selectedItems()))

        self.ui.fantasy_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.fantasy_table_widget.selectedItems()))

        self.ui.biography_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.biography_table_widget.selectedItems()))

        self.ui.history_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.history_table_widget.selectedItems()))

        self.ui.magazine_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.magazine_table_widget.selectedItems()))

        self.ui.religion_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.religion_table_widget.selectedItems()))

        self.ui.sports_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.sports_table_widget.selectedItems()))

        # Load ebooks
        self.load_ebooks()

    def checkout_ebook(self, row_items):
        book = self.model.get_book_instance(row_items[2].text())
        self.purchase_dialog = ConfirmedPurchaseDialogView(self.model,
                                                           username='visitor',
                                                           rate=book.price,
                                                           cover_img=book.cover_img,
                                                           summary=book.summary,
                                                           isbn=book.isbn,
                                                           main_window_inst=self,
                                                           )
        self.purchase_dialog.setWindowTitle('Confirm Purchase [RU Only]')
        self.purchase_dialog.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setDisabled(True)
        self.purchase_dialog.ui.length_spin_box.setDisabled(True)
        self.purchase_dialog.exec_()

    def load_ebooks(self):
        book_dict = self.model.catalogue_loader()
        row = 0
        for book in book_dict['Adventure']:
            self.ui.adventure_table_widget.insertRow(row)
            self.ui.adventure_table_widget.setItem(row, 0,
                                                   QtGui.QTableWidgetItem(book.title))
            self.ui.adventure_table_widget.setItem(row, 1,
                                                   QtGui.QTableWidgetItem(book.author))
            self.ui.adventure_table_widget.setItem(row, 2,
                                                   QtGui.QTableWidgetItem(book.isbn))
            self.ui.adventure_table_widget.setItem(row, 3,
                                                   QtGui.QTableWidgetItem(str(book.price)))
            self.ui.adventure_table_widget.setItem(row, 4,
                                                   QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.adventure_table_widget.setItem(row, 5,
                                                   QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Kids']:
            self.ui.kids_table_widget.insertRow(row)
            self.ui.kids_table_widget.setItem(row, 0,
                                              QtGui.QTableWidgetItem(book.title))
            self.ui.kids_table_widget.setItem(row, 1,
                                              QtGui.QTableWidgetItem(book.author))
            self.ui.kids_table_widget.setItem(row, 2,
                                              QtGui.QTableWidgetItem(book.isbn))
            self.ui.kids_table_widget.setItem(row, 3,
                                              QtGui.QTableWidgetItem(str(book.price)))
            self.ui.kids_table_widget.setItem(row, 4,
                                              QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.kids_table_widget.setItem(row, 5,
                                              QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Education']:
            self.ui.edu_table_widget.insertRow(row)
            self.ui.edu_table_widget.setItem(row, 0,
                                             QtGui.QTableWidgetItem(book.title))
            self.ui.edu_table_widget.setItem(row, 1,
                                             QtGui.QTableWidgetItem(book.author))
            self.ui.edu_table_widget.setItem(row, 2,
                                             QtGui.QTableWidgetItem(book.isbn))
            self.ui.edu_table_widget.setItem(row, 3,
                                             QtGui.QTableWidgetItem(str(book.price)))
            self.ui.edu_table_widget.setItem(row, 4,
                                             QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.edu_table_widget.setItem(row, 5,
                                             QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['DIY']:
            self.ui.diy_table_widget.insertRow(row)
            self.ui.diy_table_widget.setItem(row, 0,
                                             QtGui.QTableWidgetItem(book.title))
            self.ui.diy_table_widget.setItem(row, 1,
                                             QtGui.QTableWidgetItem(book.author))
            self.ui.diy_table_widget.setItem(row, 2,
                                             QtGui.QTableWidgetItem(book.isbn))
            self.ui.diy_table_widget.setItem(row, 3,
                                             QtGui.QTableWidgetItem(str(book.price)))
            self.ui.diy_table_widget.setItem(row, 4,
                                             QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.diy_table_widget.setItem(row, 5,
                                             QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Romance']:
            self.ui.romance_table_widget.insertRow(row)
            self.ui.romance_table_widget.setItem(row, 0,
                                                 QtGui.QTableWidgetItem(book.title))
            self.ui.romance_table_widget.setItem(row, 1,
                                                 QtGui.QTableWidgetItem(book.author))
            self.ui.romance_table_widget.setItem(row, 2,
                                                 QtGui.QTableWidgetItem(book.isbn))
            self.ui.romance_table_widget.setItem(row, 3,
                                                 QtGui.QTableWidgetItem(str(book.price)))
            self.ui.romance_table_widget.setItem(row, 4,
                                                 QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.romance_table_widget.setItem(row, 5,
                                                 QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Comedy']:
            self.ui.comedy_table_widget.insertRow(row)
            self.ui.comedy_table_widget.setItem(row, 0,
                                                QtGui.QTableWidgetItem(book.title))
            self.ui.comedy_table_widget.setItem(row, 1,
                                                QtGui.QTableWidgetItem(book.author))
            self.ui.comedy_table_widget.setItem(row, 2,
                                                QtGui.QTableWidgetItem(book.isbn))
            self.ui.comedy_table_widget.setItem(row, 3,
                                                QtGui.QTableWidgetItem(str(book.price)))
            self.ui.comedy_table_widget.setItem(row, 4,
                                                QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.comedy_table_widget.setItem(row, 5,
                                                QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Fantasy']:
            self.ui.fantasy_table_widget.insertRow(row)
            self.ui.fantasy_table_widget.setItem(row, 0,
                                                 QtGui.QTableWidgetItem(book.title))
            self.ui.fantasy_table_widget.setItem(row, 1,
                                                 QtGui.QTableWidgetItem(book.author))
            self.ui.fantasy_table_widget.setItem(row, 2,
                                                 QtGui.QTableWidgetItem(book.isbn))
            self.ui.fantasy_table_widget.setItem(row, 3,
                                                 QtGui.QTableWidgetItem(str(book.price)))
            self.ui.fantasy_table_widget.setItem(row, 4,
                                                 QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.fantasy_table_widget.setItem(row, 5,
                                                 QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Biography']:
            self.ui.biography_table_widget.insertRow(row)
            self.ui.biography_table_widget.setItem(row, 0,
                                                   QtGui.QTableWidgetItem(book.title))
            self.ui.biography_table_widget.setItem(row, 1,
                                                   QtGui.QTableWidgetItem(book.author))
            self.ui.biography_table_widget.setItem(row, 2,
                                                   QtGui.QTableWidgetItem(book.isbn))
            self.ui.biography_table_widget.setItem(row, 3,
                                                   QtGui.QTableWidgetItem(str(book.price)))
            self.ui.biography_table_widget.setItem(row, 4,
                                                   QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.biography_table_widget.setItem(row, 5,
                                                   QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['History']:
            self.ui.history_table_widget.insertRow(row)
            self.ui.history_table_widget.setItem(row, 0,
                                                 QtGui.QTableWidgetItem(book.title))
            self.ui.history_table_widget.setItem(row, 1,
                                                 QtGui.QTableWidgetItem(book.author))
            self.ui.history_table_widget.setItem(row, 2,
                                                 QtGui.QTableWidgetItem(book.isbn))
            self.ui.history_table_widget.setItem(row, 3,
                                                 QtGui.QTableWidgetItem(str(book.price)))
            self.ui.history_table_widget.setItem(row, 4,
                                                 QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.history_table_widget.setItem(row, 5,
                                                 QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Magazine']:
            self.ui.magazine_table_widget.insertRow(row)
            self.ui.magazine_table_widget.setItem(row, 0,
                                                  QtGui.QTableWidgetItem(book.title))
            self.ui.magazine_table_widget.setItem(row, 1,
                                                  QtGui.QTableWidgetItem(book.author))
            self.ui.magazine_table_widget.setItem(row, 2,
                                                  QtGui.QTableWidgetItem(book.isbn))
            self.ui.magazine_table_widget.setItem(row, 3,
                                                  QtGui.QTableWidgetItem(str(book.price)))
            self.ui.magazine_table_widget.setItem(row, 4,
                                                  QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.magazine_table_widget.setItem(row, 5,
                                                  QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Religion']:
            self.ui.religion_table_widget.insertRow(row)
            self.ui.religion_table_widget.setItem(row, 0,
                                                  QtGui.QTableWidgetItem(book.title))
            self.ui.religion_table_widget.setItem(row, 1,
                                                  QtGui.QTableWidgetItem(book.author))
            self.ui.religion_table_widget.setItem(row, 2,
                                                  QtGui.QTableWidgetItem(book.isbn))
            self.ui.religion_table_widget.setItem(row, 3,
                                                  QtGui.QTableWidgetItem(str(book.price)))
            self.ui.religion_table_widget.setItem(row, 4,
                                                  QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.religion_table_widget.setItem(row, 5,
                                                  QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Sports']:
            self.ui.sports_table_widget.insertRow(row)
            self.ui.sports_table_widget.setItem(row, 0,
                                                QtGui.QTableWidgetItem(book.title))
            self.ui.sports_table_widget.setItem(row, 1,
                                                QtGui.QTableWidgetItem(book.author))
            self.ui.sports_table_widget.setItem(row, 2,
                                                QtGui.QTableWidgetItem(book.isbn))
            self.ui.sports_table_widget.setItem(row, 3,
                                                QtGui.QTableWidgetItem(str(book.price)))
            self.ui.sports_table_widget.setItem(row, 4,
                                                QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.sports_table_widget.setItem(row, 5,
                                                QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

    def search(self):
        if self.ui.search_line_edit.text():
            self.ui.search_table_widget.show()
            self.ui.close_push_button.show()
            # TODO: Add search functionality when populate script is finished.
        else:
            QtGui.QMessageBox.about(self, "Error", "Empty search fields, please enter a genre, title, etc.")

    def close_search(self):
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()

    def register(self):
        self.hide()
        self.register_view.show()

    def login(self):
        self.hide()
        self.login_view.show()


class MainWindowRegisteredView(QtGui.QMainWindow):
    def __init__(self, model, username):
        self.model = model
        self.purchase_dialog = None
        self.username = username
        self.user_instance = load_serialized_user(self.username)
        self.admin_view = None
        self.upload_view = UploadFormView(self.model, username, self)
        self.reader_view = None
        super(MainWindowRegisteredView, self).__init__()
        self.ui = Ui_MainWindowRegistered.Ui_MainWindow()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Default text in Search Line Edit
        self.ui.search_line_edit.setPlaceholderText('Search...')

        # Hide results table widget for later
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()
        self.ui.library_table_widget.hide()
        self.ui.read_library_push_button.hide()

        self.ui.go_push_button.clicked.connect(self.search)
        self.ui.close_push_button.clicked.connect(self.close_search)
        self.ui.search_line_edit.returnPressed.connect(self.search)
        self.ui.upload_push_button.clicked.connect(self.upload)
        self.ui.library_push_button.clicked.connect(self.library)
        self.ui.admin_push_button.clicked.connect(self.admin)

        self.ui.read_library_push_button.clicked.connect(lambda: self.read_book(
            self.ui.library_table_widget.selectedItems()[2].text()
        ))

        if self.user_instance.group_policy == 'RU':
            self.ui.admin_push_button.hide()

        # Load the user/ebook info
        self.reload_user_info()
        self.load_ebooks()

        # Connect checkout buttons
        self.ui.kids_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.kids_table_widget.selectedItems()))

        self.ui.top_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.top_table_widget.selectedItems()))

        self.ui.adventure_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.adventure_table_widget.selectedItems()))

        self.ui.edu_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.edu_table_widget.selectedItems()))

        self.ui.diy_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.diy_table_widget.selectedItems()))

        self.ui.romance_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.romance_table_widget.selectedItems()))

        self.ui.comedy_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.comedy_table_widget.selectedItems()))

        self.ui.fantasy_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.fantasy_table_widget.selectedItems()))

        self.ui.biography_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.biography_table_widget.selectedItems()))

        self.ui.history_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.history_table_widget.selectedItems()))

        self.ui.magazine_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.magazine_table_widget.selectedItems()))

        self.ui.religion_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.religion_table_widget.selectedItems()))

        self.ui.sports_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.sports_table_widget.selectedItems()))

    def reload_user_info(self):
        self.user_instance = load_serialized_user(self.username)
        self.ui.username_label.setText('Hello, ' + self.username)
        self.ui.reputation_label.setText('Credits: ' + str(self.user_instance.credits))
        self.load_library_books()

    def checkout_ebook(self, row_items):
        book = self.model.get_book_instance(row_items[2].text())
        self.purchase_dialog = ConfirmedPurchaseDialogView(self.model,
                                                           username=self.username,
                                                           rate=book.price,
                                                           cover_img=book.cover_img,
                                                           summary=book.summary,
                                                           isbn=book.isbn,
                                                           main_window_inst=self,
                                                           )
        self.purchase_dialog.exec_()

    def load_library_books(self):
        self.ui.library_table_widget.setRowCount(0)
        row = 0
        rented_books_instances = []
        if len(self.user_instance.rented_books) > 0:
            for book_isbn_key in self.user_instance.rented_books.keys():
                rented_books_instances.append(load_serialized_ebook(book_isbn_key))

        for book in rented_books_instances:
            self.ui.library_table_widget.insertRow(row)
            self.ui.library_table_widget.setItem(row, 0,
                                                 QtGui.QTableWidgetItem(book.title))
            self.ui.library_table_widget.setItem(row, 1,
                                                 QtGui.QTableWidgetItem(book.author))
            self.ui.library_table_widget.setItem(row, 2,
                                                 QtGui.QTableWidgetItem(book.isbn))
            self.ui.library_table_widget.setItem(row, 3,
                                                 QtGui.QTableWidgetItem(str(book.price)))
            self.ui.library_table_widget.setItem(row, 4,
                                                 QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.library_table_widget.setItem(row, 5,
                                                 QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

    def load_ebooks(self):
        # Remove rows if exists
        self.ui.kids_table_widget.setRowCount(0)
        self.ui.adventure_table_widget.setRowCount(0)
        self.ui.top_table_widget.setRowCount(0)
        self.ui.edu_table_widget.setRowCount(0)
        self.ui.diy_table_widget.setRowCount(0)
        self.ui.romance_table_widget.setRowCount(0)
        self.ui.comedy_table_widget.setRowCount(0)
        self.ui.fantasy_table_widget.setRowCount(0)
        self.ui.biography_table_widget.setRowCount(0)
        self.ui.history_table_widget.setRowCount(0)
        self.ui.magazine_table_widget.setRowCount(0)
        self.ui.religion_table_widget.setRowCount(0)
        self.ui.sports_table_widget.setRowCount(0)

        self.load_library_books()

        book_dict = self.model.catalogue_loader()
        row = 0
        for book in book_dict['Adventure']:
            self.ui.adventure_table_widget.insertRow(row)
            self.ui.adventure_table_widget.setItem(row, 0,
                                                   QtGui.QTableWidgetItem(book.title))
            self.ui.adventure_table_widget.setItem(row, 1,
                                                   QtGui.QTableWidgetItem(book.author))
            self.ui.adventure_table_widget.setItem(row, 2,
                                                   QtGui.QTableWidgetItem(book.isbn))
            self.ui.adventure_table_widget.setItem(row, 3,
                                                   QtGui.QTableWidgetItem(str(book.price)))
            self.ui.adventure_table_widget.setItem(row, 4,
                                                   QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.adventure_table_widget.setItem(row, 5,
                                                   QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Kids']:
            self.ui.kids_table_widget.insertRow(row)
            self.ui.kids_table_widget.setItem(row, 0,
                                              QtGui.QTableWidgetItem(book.title))
            self.ui.kids_table_widget.setItem(row, 1,
                                              QtGui.QTableWidgetItem(book.author))
            self.ui.kids_table_widget.setItem(row, 2,
                                              QtGui.QTableWidgetItem(book.isbn))
            self.ui.kids_table_widget.setItem(row, 3,
                                              QtGui.QTableWidgetItem(str(book.price)))
            self.ui.kids_table_widget.setItem(row, 4,
                                              QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.kids_table_widget.setItem(row, 5,
                                              QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Education']:
            self.ui.edu_table_widget.insertRow(row)
            self.ui.edu_table_widget.setItem(row, 0,
                                             QtGui.QTableWidgetItem(book.title))
            self.ui.edu_table_widget.setItem(row, 1,
                                             QtGui.QTableWidgetItem(book.author))
            self.ui.edu_table_widget.setItem(row, 2,
                                             QtGui.QTableWidgetItem(book.isbn))
            self.ui.edu_table_widget.setItem(row, 3,
                                             QtGui.QTableWidgetItem(str(book.price)))
            self.ui.edu_table_widget.setItem(row, 4,
                                             QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.edu_table_widget.setItem(row, 5,
                                             QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['DIY']:
            self.ui.diy_table_widget.insertRow(row)
            self.ui.diy_table_widget.setItem(row, 0,
                                             QtGui.QTableWidgetItem(book.title))
            self.ui.diy_table_widget.setItem(row, 1,
                                             QtGui.QTableWidgetItem(book.author))
            self.ui.diy_table_widget.setItem(row, 2,
                                             QtGui.QTableWidgetItem(book.isbn))
            self.ui.diy_table_widget.setItem(row, 3,
                                             QtGui.QTableWidgetItem(str(book.price)))
            self.ui.diy_table_widget.setItem(row, 4,
                                             QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.diy_table_widget.setItem(row, 5,
                                             QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Romance']:
            self.ui.romance_table_widget.insertRow(row)
            self.ui.romance_table_widget.setItem(row, 0,
                                                 QtGui.QTableWidgetItem(book.title))
            self.ui.romance_table_widget.setItem(row, 1,
                                                 QtGui.QTableWidgetItem(book.author))
            self.ui.romance_table_widget.setItem(row, 2,
                                                 QtGui.QTableWidgetItem(book.isbn))
            self.ui.romance_table_widget.setItem(row, 3,
                                                 QtGui.QTableWidgetItem(str(book.price)))
            self.ui.romance_table_widget.setItem(row, 4,
                                                 QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.romance_table_widget.setItem(row, 5,
                                                 QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Comedy']:
            self.ui.comedy_table_widget.insertRow(row)
            self.ui.comedy_table_widget.setItem(row, 0,
                                                QtGui.QTableWidgetItem(book.title))
            self.ui.comedy_table_widget.setItem(row, 1,
                                                QtGui.QTableWidgetItem(book.author))
            self.ui.comedy_table_widget.setItem(row, 2,
                                                QtGui.QTableWidgetItem(book.isbn))
            self.ui.comedy_table_widget.setItem(row, 3,
                                                QtGui.QTableWidgetItem(str(book.price)))
            self.ui.comedy_table_widget.setItem(row, 4,
                                                QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.comedy_table_widget.setItem(row, 5,
                                                QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Fantasy']:
            self.ui.fantasy_table_widget.insertRow(row)
            self.ui.fantasy_table_widget.setItem(row, 0,
                                                 QtGui.QTableWidgetItem(book.title))
            self.ui.fantasy_table_widget.setItem(row, 1,
                                                 QtGui.QTableWidgetItem(book.author))
            self.ui.fantasy_table_widget.setItem(row, 2,
                                                 QtGui.QTableWidgetItem(book.isbn))
            self.ui.fantasy_table_widget.setItem(row, 3,
                                                 QtGui.QTableWidgetItem(str(book.price)))
            self.ui.fantasy_table_widget.setItem(row, 4,
                                                 QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.fantasy_table_widget.setItem(row, 5,
                                                 QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Biography']:
            self.ui.biography_table_widget.insertRow(row)
            self.ui.biography_table_widget.setItem(row, 0,
                                                   QtGui.QTableWidgetItem(book.title))
            self.ui.biography_table_widget.setItem(row, 1,
                                                   QtGui.QTableWidgetItem(book.author))
            self.ui.biography_table_widget.setItem(row, 2,
                                                   QtGui.QTableWidgetItem(book.isbn))
            self.ui.biography_table_widget.setItem(row, 3,
                                                   QtGui.QTableWidgetItem(str(book.price)))
            self.ui.biography_table_widget.setItem(row, 4,
                                                   QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.biography_table_widget.setItem(row, 5,
                                                   QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['History']:
            self.ui.history_table_widget.insertRow(row)
            self.ui.history_table_widget.setItem(row, 0,
                                                 QtGui.QTableWidgetItem(book.title))
            self.ui.history_table_widget.setItem(row, 1,
                                                 QtGui.QTableWidgetItem(book.author))
            self.ui.history_table_widget.setItem(row, 2,
                                                 QtGui.QTableWidgetItem(book.isbn))
            self.ui.history_table_widget.setItem(row, 3,
                                                 QtGui.QTableWidgetItem(str(book.price)))
            self.ui.history_table_widget.setItem(row, 4,
                                                 QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.history_table_widget.setItem(row, 5,
                                                 QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Magazine']:
            self.ui.magazine_table_widget.insertRow(row)
            self.ui.magazine_table_widget.setItem(row, 0,
                                                  QtGui.QTableWidgetItem(book.title))
            self.ui.magazine_table_widget.setItem(row, 1,
                                                  QtGui.QTableWidgetItem(book.author))
            self.ui.magazine_table_widget.setItem(row, 2,
                                                  QtGui.QTableWidgetItem(book.isbn))
            self.ui.magazine_table_widget.setItem(row, 3,
                                                  QtGui.QTableWidgetItem(str(book.price)))
            self.ui.magazine_table_widget.setItem(row, 4,
                                                  QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.magazine_table_widget.setItem(row, 5,
                                                  QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Religion']:
            self.ui.religion_table_widget.insertRow(row)
            self.ui.religion_table_widget.setItem(row, 0,
                                                  QtGui.QTableWidgetItem(book.title))
            self.ui.religion_table_widget.setItem(row, 1,
                                                  QtGui.QTableWidgetItem(book.author))
            self.ui.religion_table_widget.setItem(row, 2,
                                                  QtGui.QTableWidgetItem(book.isbn))
            self.ui.religion_table_widget.setItem(row, 3,
                                                  QtGui.QTableWidgetItem(str(book.price)))
            self.ui.religion_table_widget.setItem(row, 4,
                                                  QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.religion_table_widget.setItem(row, 5,
                                                  QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

        row = 0
        for book in book_dict['Sports']:
            self.ui.sports_table_widget.insertRow(row)
            self.ui.sports_table_widget.setItem(row, 0,
                                                QtGui.QTableWidgetItem(book.title))
            self.ui.sports_table_widget.setItem(row, 1,
                                                QtGui.QTableWidgetItem(book.author))
            self.ui.sports_table_widget.setItem(row, 2,
                                                QtGui.QTableWidgetItem(book.isbn))
            self.ui.sports_table_widget.setItem(row, 3,
                                                QtGui.QTableWidgetItem(str(book.price)))
            self.ui.sports_table_widget.setItem(row, 4,
                                                QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.sports_table_widget.setItem(row, 5,
                                                QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

    def search(self):
        if self.ui.search_line_edit.text():
            self.ui.search_table_widget.show()
            self.ui.close_push_button.show()

    def close_search(self):
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()

    def upload(self):
        self.hide()
        self.upload_view.show()

    def library(self):
        if self.ui.library_table_widget.isHidden():
            self.ui.library_table_widget.show()
            self.ui.read_library_push_button.show()
        else:
            self.ui.library_table_widget.hide()
            self.ui.read_library_push_button.hide()

    def admin(self):
        self.admin_view = ApprovalReportedMainView(self.model, self.username)
        self.admin_view.show()
        self.hide()

    def read_book(self, book_isbn):
        self.reader_view = ReaderFormView(self.model, self, book_isbn, self.user_instance)
        self.reader_view.show()
        self.hide()


class ApprovalReportedMainView(QtGui.QWidget):
    def __init__(self, model, username):
        self.model = model
        self.username = username
        self.user_file = load_serialized_user(self.username)
        self.reputation = self.user_file.credits
        super(ApprovalReportedMainView, self).__init__()
        self.ui = Ui_ApprovalReportedList.Ui_Form()
        self.build_ui()
        self.main_view = None

    def build_ui(self):
        self.ui.setupUi(self)

        self.ui.approve_push_button.clicked.connect(self.approve)
        self.ui.delete_push_button.clicked.connect(self.delete)
        self.ui.cancel_push_button.clicked.connect(self.cancel)

    def approve(self):
        print "approve clicked"

    def delete(self):
        print "delete clicked"

    def cancel(self):
        print "cancel clicked"
        self.main_view = MainWindowRegisteredView(self.model, self.username)
        self.main_view.show()
        self.hide()
