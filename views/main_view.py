from PySide import QtGui, QtCore
from ui import Ui_UploadForm, Ui_ReaderForm, Ui_ReportDialog, Ui_LoginForm, Ui_RegisterForm, Ui_MainWindowVisitor, \
    Ui_MainWindowRegistered, Ui_ConfirmPurchaseDialog, Ui_ApprovalReportedList, Ui_BadWordsDialog, Ui_ReviewRateDialog, \
    Ui_ShareBookDialog, Ui_ShareRequestWidget
from models.main_model import submit_upload_form, submit_report_form, submit_review_rate_form, review_exists, \
    report_exists, user_exists
from database.database_objects import load_serialized_user, load_serialized_ebook, PurchasedEBook, serialize_user, \
    update_serialized_ebook, update_serialized_user
from recommendations import get_top_related_books
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
        if len(self.ui.isbn_line_edit.text()) == 10:
            if self.ui.title_line_edit.text() and self.ui.author_line_edit.text():
                does_file_exist = os.path.isfile(self.file_location)
                if does_file_exist:
                    # File uploaded successfully
                    submit_upload_form(title=self.ui.title_line_edit.text(),
                                       author=self.ui.author_line_edit.text(),
                                       genre=self.ui.genres_combo_box.currentText(),
                                       isbn=self.ui.isbn_line_edit.text(),
                                       price=self.ui.price_spin_box.value(),
                                       uploader=self.username,
                                       summary=self.ui.summary_plain_text_edit.toPlainText(),
                                       cover_img=self.cover_img_location,
                                       file_location=self.file_location,
                                       )
                    self.new_book_added = True
                    self.close()
                else:
                    # Returns an Error message if file DNE
                    QtGui.QMessageBox.about(self, "Invalid PDF", "PDF file does not exist: " + str(self.file_location))
            else:
                QtGui.QMessageBox.about(self, "Error", "Fields must be filled in.")
        else:
            QtGui.QMessageBox.about(self, "ISBN Error", "ISBN must be of length 10")

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
        self.queue_counter = 0
        super(ConfirmedPurchaseDialogView, self).__init__()
        self.ui = Ui_ConfirmPurchaseDialog.Ui_Dialog()
        self.build_ui()

        # Load the user info + book info
        self.user_instance = load_serialized_user(self.username)
        self.ebook_in_transaction = load_serialized_ebook(self.isbn)
        self.ui.num_of_purchases_label.setText(str(self.ebook_in_transaction.buy_count))
        self.ui.total_seconds_label.setText(str(self.ebook_in_transaction.total_seconds))

        # Set up reviews queue
        reviews_list = self.model.get_reviews_queue(self.isbn)
        if reviews_list is not None:
            self.ui.review_text_browser.setText(
                reviews_list[self.queue_counter].review + '\nPosted by ' +
                reviews_list[self.queue_counter].reviewer.username)
            if len(reviews_list) > 1:
                self.ui.next_review_push_button.clicked.connect(
                    lambda: self.next_review(reviews_list)
                )
            else:
                self.ui.next_review_push_button.hide()
        else:
            self.ui.review_text_browser.hide()
            self.ui.next_review_push_button.hide()
            self.ui.review_label.hide()

    def build_ui(self):
        self.ui.setupUi(self)

        self.ui.summary_text_browser.setText(self.summary)
        self.ui.cover_img_web_view.setHtml('<img alt="Cover img" '
                                           'src="' + self.cover_img + '" style="width: 300px; height: 300px">')
        self.ui.cost_label.setText(str(self.rate))

    def accept(self, *args, **kwargs):
        transaction_price = self.ebook_in_transaction.price * self.ui.length_spin_box.value()
        # if self.user_instance.credits >= transaction_price:
        #     ebook_purchase = PurchasedEBook(self.username,
        #                                     self.isbn,
        #                                     datetime.datetime.now(),
        #                                     self.ui.length_spin_box.value(),
        #                                     datetime.datetime.now(),
        #                                     transaction_price)
        #     self.user_instance.credits -= transaction_price
        #     self.user_instance.rented_books[self.isbn] = ebook_purchase
        #     # Increment buy count in EBook
        #     self.ebook_in_transaction.buy_count += 1
        #     update_serialized_ebook(self.ebook_in_transaction)
        if self.user_instance.credits >= self.ebook_in_transaction.price * self.ui.length_spin_box.value():
            if self.isbn in self.user_instance.rented_books.keys():
                self.user_instance.rented_books[self.isbn].length_on_rent += self.ui.length_spin_box.value()
            else:
                ebook_purchase = PurchasedEBook(self.username,
                                                self.isbn,
                                                datetime.datetime.now(),
                                                self.ui.length_spin_box.value(),
                                                datetime.datetime.now(),
                                                0)

                self.user_instance.rented_books[self.isbn] = ebook_purchase

            self.user_instance.credits -= (self.ebook_in_transaction.price * self.ui.length_spin_box.value())
            serialize_user(self.user_instance, self.user_instance.__unicode__)
            self.main_window.reload_user_info()
            self.hide()
        else:
            print 'NOT ENOUGH CREDITS TO PURCHASE ' + self.ebook_in_transaction.title
            QtGui.QMessageBox.about(self, "Insufficient funds", "You don't have enough credits for that much time!")

    def next_review(self, reviews_list):
        self.queue_counter += 1
        if self.queue_counter >= len(reviews_list):
            self.queue_counter = 0
        self.ui.review_text_browser.setText(
            reviews_list[self.queue_counter].review + '\nPosted by ' +
            reviews_list[self.queue_counter].reviewer.username
        )


class ReportDialogView(QtGui.QDialog):
    def __init__(self, model, book_instance, reporter, report_push_button, reason=""):
        self.model = model
        super(ReportDialogView, self).__init__()
        self.ui = Ui_ReportDialog.Ui_Dialog()
        self.reporter = reporter
        self.report_push_button = report_push_button
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

        print "reason: " + reason
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
                submit_report_form(self.reporter, report_selection, report_description, self.book_instance)
                self.report_push_button.setDisabled(True)
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

        self.timer = QtCore.QTimer(self)
        self.paused = True
        self.pdf_reader_location = None
        self.reader_process = None
        self.build_ui()

        self.count_seconds = 0
        self.review_rate_dialog = ReviewRateDialogView(self.model, self.book_instance, self.user_instance,
                                                       self.ui.review_rate_push_button)
        self.report_dialog = ReportDialogView(self.model, self.book_instance, self.user_instance,
                                              self.ui.report_push_button)
        self.share_dialog = ShareBookDialogView(self.model, self.main_window, self.user_instance.username,
                                                self.book_instance.isbn)

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
            self.book_instance.update_last_time_read()
            self.user_instance.rented_books[self.book_instance.isbn].count_seconds = self.count_seconds
            self.user_instance.rented_books[self.book_instance.isbn].add_seconds(self.count_seconds)

            update_serialized_user(self.user_instance)
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

        self.book_instance.add_seconds(self.count_seconds)
        self.book_instance.update_last_time_read()
        self.user_instance.rented_books[self.book_instance.isbn].count_seconds = self.count_seconds
        self.user_instance.rented_books[self.book_instance.isbn].add_seconds(self.count_seconds)

        update_serialized_user(self.user_instance)
        update_serialized_ebook(self.book_instance)

    @QtCore.Slot()
    def share(self):
        # Trigger the share widget
        if self.user_instance.rented_books[self.book_instance.isbn].length_on_rent <= 1:
            QtGui.QMessageBox.about(self, "Error", "You do not have enough time left to share this book.")
        else:
            self.share_dialog.show()

    @QtCore.Slot()
    def report(self):
        # Trigger the report widget
        if not report_exists(self.user_instance, self.book_instance):
            self.report_dialog.show()
        else:
            QtGui.QMessageBox.about(self, "Error", "You have already reported this book once!")

    @QtCore.Slot()
    def review_rate(self):
        # Trigger the report widget
        if not review_exists(self.user_instance, self.book_instance):
            self.review_rate_dialog.show()
        else:
            QtGui.QMessageBox.about(self, "Error", "You have already reviewed/rated this book once!")

    @QtCore.Slot()
    def browse_reader_location(self):
        pdf_reader = QtGui.QFileDialog.getOpenFileName(self, 'Open PDF Reader', '',
                                                       'PDF Reader Formats (*.exe)')
        if pdf_reader[1]:
            self.ui.pdf_reader_path_label.setText(pdf_reader[0])
            self.pdf_reader_location = pdf_reader[0]

    def closeEvent(self, *args, **kwargs):
        self.user_instance.rented_books[self.book_instance.isbn].reset_count_seconds()
        self.user_instance.default_pdf_reader = self.pdf_reader_location
        serialize_user(self.user_instance, self.user_instance.username)
        self.main_window.show()
        self.hide()


class ReviewRateDialogView(QtGui.QDialog):
    def __init__(self, model, book_instance, reviewer, review_rate_push_button):
        self.model = model
        super(ReviewRateDialogView, self).__init__()
        self.ui = Ui_ReviewRateDialog.Ui_Dialog()

        self.book_instance = book_instance
        self.reviewer = reviewer
        self.review_rate_push_button = review_rate_push_button
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Setup combo box
        self.ui.rating_combo_box.addItems(["", "1", "2", "3", "4", "5"])

        self.ui.submit_push_button.clicked.connect(self.submit)

    @QtCore.Slot()
    def submit(self):
        review_text = self.ui.review_text_edit.toPlainText()

        if self.ui.rating_combo_box == "":
            # Display an error message to tell the user to give a rating
            QtGui.QMessageBox.about(self, "Error", "You have not yet selected a rating")
        elif review_text == "":
            # Display an error message to tell the user to write a description
            QtGui.QMessageBox.about(self, "Error", "You have not yet written anything in the review")
        else:
            if self.book_instance.total_seconds == 0.0 or \
                            self.reviewer.rented_books[self.book_instance.isbn].total_seconds == 0:
                # Display an error message to tell the user to read the book first! (Calculate rating when division
                # by 0 is undefined!)
                QtGui.QMessageBox.about(self, "Error", 'You have not even read the book yet! '
                                                       'Come back to review once you\'ve read for at least a second')
                return

            submit_review_rate_form(self.book_instance, self.reviewer,
                                    float(self.ui.rating_combo_box.currentText()),
                                    review_text)

            self.review_rate_push_button.setDisabled(True)
            self.hide()


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
                if load_serialized_user(username).is_blacklisted:
                    QtGui.QMessageBox.about(self, "Account Banned!", "This account has been banned due to multiple"
                                                                     " infractions!");
                else:
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
            if load_serialized_user(username).is_blacklisted:
                QtGui.QMessageBox.about(self, "Banned Account!", "This user cannot register as this instance has been"
                                                                 " banned.")
            elif load_serialized_user(
                    username) is not None and password == confirm_password and not load_serialized_user(
                    username).is_blacklisted:
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

        row = 0
        for book in book_dict['TOP']:
            self.ui.top_table_widget.insertRow(row)
            self.ui.top_table_widget.setItem(row, 0,
                                             QtGui.QTableWidgetItem(book.title))
            self.ui.top_table_widget.setItem(row, 1,
                                             QtGui.QTableWidgetItem(book.author))
            self.ui.top_table_widget.setItem(row, 2,
                                             QtGui.QTableWidgetItem(book.isbn))
            self.ui.top_table_widget.setItem(row, 3,
                                             QtGui.QTableWidgetItem(str(book.price)))
            self.ui.top_table_widget.setItem(row, 4,
                                             QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.top_table_widget.setItem(row, 5,
                                             QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

    def search(self):
        if self.ui.search_line_edit.text():
            self.ui.search_table_widget.show()
            self.ui.close_push_button.show()
            self.ui.search_table_widget.setRowCount(0)
            for row, result_book in enumerate(self.model.search(self.ui.search_line_edit.text())):
                self.ui.search_table_widget.insertRow(row)
                self.ui.search_table_widget.setItem(row, 0,
                                                    QtGui.QTableWidgetItem(result_book.title))
                self.ui.search_table_widget.setItem(row, 1,
                                                    QtGui.QTableWidgetItem(result_book.author))
                self.ui.search_table_widget.setItem(row, 2,
                                                    QtGui.QTableWidgetItem(result_book.isbn))
                self.ui.search_table_widget.setItem(row, 3,
                                                    QtGui.QTableWidgetItem(str(result_book.price)))
                self.ui.search_table_widget.setItem(row, 4,
                                                    QtGui.QTableWidgetItem(result_book.uploader.username))
                self.ui.search_table_widget.setItem(row, 5,
                                                    QtGui.QTableWidgetItem(str(result_book.rating)))
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
        self.infraction_message_box = None
        self.upload_view = UploadFormView(self.model, username, self)
        self.reader_view = None
        self.request_view = None
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
        self.ui.search_checkout_push_button.hide()

        self.ui.go_push_button.clicked.connect(self.search)
        self.ui.close_push_button.clicked.connect(self.close_search)
        self.ui.search_line_edit.returnPressed.connect(self.search)
        self.ui.upload_push_button.clicked.connect(self.upload)
        self.ui.library_push_button.clicked.connect(self.library)
        self.ui.admin_push_button.clicked.connect(self.admin)
        self.ui.check_share_request_push_button.clicked.connect(self.share_request)

        self.ui.read_library_push_button.clicked.connect(lambda: self.read_book(
            self.ui.library_table_widget.selectedItems()[2].text()
        ))

        if self.user_instance.group_policy == 'RU':
            self.ui.admin_push_button.hide()

        # Load the user/ebook info
        self.reload_user_info()
        self.load_ebooks()
        self.load_recommended_books()

        # self.ui.action_infractions.triggered.connnect(self.trigger_infraction_message_box)

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

        # Search checkout
        self.ui.search_checkout_push_button.clicked.connect(lambda: self.checkout_ebook(
            self.ui.search_table_widget.selectedItems()))

    def trigger_infraction_message_box(self):
        self.infraction_message_box = QtGui.QMessageBox(self)
        self.infraction_message_box.setText(len(self.user_instance.infractions.values()))

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
            self.user_instance = load_serialized_user(self.user_instance.username)
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

    def load_recommended_books(self):
        self.ui.saved_table_widget.setRowCount(0)
        similar_books = get_top_related_books(self.user_instance)

        row = 0
        for book in similar_books:
            self.ui.saved_table_widget.insertRow(row)
            self.ui.saved_table_widget.setItem(row, 0,
                                               QtGui.QTableWidgetItem(book.title))
            self.ui.saved_table_widget.setItem(row, 1,
                                               QtGui.QTableWidgetItem(book.author))
            self.ui.saved_table_widget.setItem(row, 2,
                                               QtGui.QTableWidgetItem(book.isbn))
            self.ui.saved_table_widget.setItem(row, 3,
                                               QtGui.QTableWidgetItem(str(book.price)))
            self.ui.saved_table_widget.setItem(row, 4,
                                               QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.saved_table_widget.setItem(row, 5,
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

        row = 0
        for book in book_dict['TOP']:
            self.ui.top_table_widget.insertRow(row)
            self.ui.top_table_widget.setItem(row, 0,
                                             QtGui.QTableWidgetItem(book.title))
            self.ui.top_table_widget.setItem(row, 1,
                                             QtGui.QTableWidgetItem(book.author))
            self.ui.top_table_widget.setItem(row, 2,
                                             QtGui.QTableWidgetItem(book.isbn))
            self.ui.top_table_widget.setItem(row, 3,
                                             QtGui.QTableWidgetItem(str(book.price)))
            self.ui.top_table_widget.setItem(row, 4,
                                             QtGui.QTableWidgetItem(book.uploader.username))
            self.ui.top_table_widget.setItem(row, 5,
                                             QtGui.QTableWidgetItem(str(book.rating)))
            row += 1

    def search(self):
        if self.ui.search_line_edit.text():
            self.ui.search_table_widget.show()
            self.ui.close_push_button.show()
            self.ui.search_checkout_push_button.show()
            self.ui.search_table_widget.setRowCount(0)
            for row, result_book in enumerate(self.model.search(self.ui.search_line_edit.text())):
                self.ui.search_table_widget.insertRow(row)
                self.ui.search_table_widget.setItem(row, 0,
                                                    QtGui.QTableWidgetItem(result_book.title))
                self.ui.search_table_widget.setItem(row, 1,
                                                    QtGui.QTableWidgetItem(result_book.author))
                self.ui.search_table_widget.setItem(row, 2,
                                                    QtGui.QTableWidgetItem(result_book.isbn))
                self.ui.search_table_widget.setItem(row, 3,
                                                    QtGui.QTableWidgetItem(str(result_book.price)))
                self.ui.search_table_widget.setItem(row, 4,
                                                    QtGui.QTableWidgetItem(result_book.uploader.username))
                self.ui.search_table_widget.setItem(row, 5,
                                                    QtGui.QTableWidgetItem(str(result_book.rating)))

    def close_search(self):
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()
        self.ui.search_checkout_push_button.hide()

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
        self.admin_view = ApprovalReportedMainView(self.model, self.username, self,
                                                   self.user_instance.default_pdf_reader)
        self.admin_view.show()
        self.hide()

    def read_book(self, book_isbn):
        self.reader_view = ReaderFormView(self.model, self, book_isbn, self.user_instance)
        self.reader_view.show()
        self.hide()

    def share_request(self):
        self.request_view = ShareRequestFormView(self.model, self, self.user_instance)
        self.request_view.show()


class ApprovalReportedMainView(QtGui.QWidget):
    def __init__(self, model, username, main_window, pdf_reader_location):
        self.model = model
        self.username = username
        self.main_window = main_window
        self.reader_process = None
        self.reports_message_box = QtGui.QMessageBox()
        self.pdf_reader_location = pdf_reader_location
        self.user_file = load_serialized_user(self.username)
        self.reputation = self.user_file.credits
        super(ApprovalReportedMainView, self).__init__()
        self.ui = Ui_ApprovalReportedList.Ui_Form()
        self.build_ui()
        self.main_view = None

    def build_ui(self):
        self.ui.setupUi(self)

        self.ui.verify_approval_push_button.clicked.connect(
            lambda: self.verify_approval(self.ui.approvals_table_widget.selectedItems()))
        self.ui.verify_reports_push_button.clicked.connect(
            lambda: self.verify_report(self.ui.reports_table_widget.selectedItems()))
        self.ui.cancel_push_button.clicked.connect(self.closeEvent)

        self.ui.remove_book_push_button.clicked.connect(
            lambda: self.remove_book_with_infraction(self.ui.reports_table_widget.selectedItems())
        )

        # Ban user connect
        self.ui.blacklist_ru_push_button.clicked.connect(
            lambda: self.blacklist_user(self.ui.reports_table_widget.selectedItems())
        )
        # Load books awaiting approval and reports
        self.books_waiting()
        self.reports_waiting()

        self.ui.approve_push_button.clicked.connect(
            lambda: self.approve(self.ui.approvals_table_widget.selectedItems())
        )

        # Load PDF reader location
        if self.pdf_reader_location is not None:
            self.ui.pdf_location_label.setText(self.pdf_reader_location)

        self.ui.pdf_reader_push_button.clicked.connect(self.browse_pdf_reader)

    def blacklist_user(self, row_items):
        self.model.blacklist_book_uploader(row_items[0].text())
        self.reports_message_box.setText('Uploader of PDF has been banned')
        self.reports_message_box.exec_()

    def browse_pdf_reader(self):
        self.pdf_reader_location = QtGui.QFileDialog.getOpenFileName(self, 'Open PDF Reader', '',
                                                                     'PDF Reader Formats (*.exe)')[0]
        self.ui.pdf_location_label.setText(self.pdf_reader_location)

    def verify_approval(self, row_items):
        self.reader_process = QtCore.QProcess(self)
        pdf = os.path.join('database', 'blobs', 'ebooks', row_items[0].text() + '.pdf')
        self.reader_process.start(self.pdf_reader_location, [pdf])

    def approve(self, row_items):
        book = load_serialized_ebook(row_items[0].text())
        if self.ui.credit_amount_spin_box.value() >= int(row_items[2].text()):
            self.model.add_user_credits(row_items[1].text(),
                                        self.ui.credit_amount_spin_box.value())
            book.approved = True
            book.award_amount = self.ui.credit_amount_spin_box.value()
            update_serialized_ebook(book)
        else:
            # Set notifier to see if uploader will accept the reduced reward
            # Second pass contains a tuple which has the values of the original requested amount
            # and the value that the SU is offering.
            book.second_pass = (int(row_items[2].text()),
                                self.ui.credit_amount_spin_box.value())
            update_serialized_ebook(book)

        self.main_window.reload_user_info()
        self.main_window.load_ebooks()
        self.books_waiting()

    def verify_report(self, row_items):
        self.reports_message_box.setText(self.model.report_info(
            row_items[0].text() + '-' + row_items[3].text().replace(':', '-')).description)
        self.reports_message_box.exec_()

    def remove_book_with_infraction(self, row_items):
        self.model.remove_ebook_with_infraction(row_items[0].text(),
                                                row_items[1].text(),
                                                row_items[3].text())
        self.reports_waiting()
        self.main_window.load_ebooks()
        self.main_window.reload_user_info()

    def books_waiting(self):
        self.ui.approvals_table_widget.setRowCount(0)
        for row, result_book in enumerate(self.model.not_approved_ebooks()):
            self.ui.approvals_table_widget.insertRow(row)
            self.ui.approvals_table_widget.setItem(row, 0,
                                                   QtGui.QTableWidgetItem(result_book.isbn))
            self.ui.approvals_table_widget.setItem(row, 1,
                                                   QtGui.QTableWidgetItem(result_book.uploader.username))
            self.ui.approvals_table_widget.setItem(row, 2,
                                                   QtGui.QTableWidgetItem(str(result_book.price)))

    def reports_waiting(self):
        self.ui.reports_table_widget.setRowCount(0)
        for row, report in enumerate(self.model.reports_list()):
            self.ui.reports_table_widget.insertRow(row)
            self.ui.reports_table_widget.setItem(row, 0,
                                                 QtGui.QTableWidgetItem(report.isbn))
            self.ui.reports_table_widget.setItem(row, 1,
                                                 QtGui.QTableWidgetItem(report.reason))
            self.ui.reports_table_widget.setItem(row, 2,
                                                 QtGui.QTableWidgetItem(str(report.reporter.username)))
            self.ui.reports_table_widget.setItem(row, 3,
                                                 QtGui.QTableWidgetItem(
                                                     str(report.time_stamp)))

    def closeEvent(self, *args, **kwargs):
        self.main_window.show()
        self.hide()
        super(ApprovalReportedMainView, self).closeEvent()


class ShareBookDialogView(QtGui.QDialog):
    def __init__(self, model, main_window, owner, isbn):
        self.model = model
        self.owner = owner
        self.isbn = isbn
        super(ShareBookDialogView, self).__init__()
        self.ui = Ui_ShareBookDialog.Ui_Dialog()
        self.owner_instance = load_serialized_user(self.owner)
        self.user_instance = None
        self.book_instance = load_serialized_ebook(self.isbn)
        self.main_window = main_window
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)
        self.ui.user_line_edit.setPlaceholderText("User")

    def accept(self, *args, **kwargs):
        # Press OK
        username = self.ui.user_line_edit.text()
        self.user_instance = load_serialized_user(username)

        # Checks if username is valid
        if not user_exists(username):
            QtGui.QMessageBox.about(self, "Error", "Invalid User")
        else:
            # Checks if user is blacklisted
            if self.user_instance.is_blacklisted:
                QtGui.QMessageBox.about(self, "Account Banned!", "This account has been banned due to multiple"
                                                                 " infractions!")
            else:
                time_left = self.owner_instance.rented_books[self.isbn].length_on_rent // 2
                e_book_shared = PurchasedEBook(self.user_instance.username,
                                               self.isbn,
                                               datetime.datetime.now(),
                                               time_left,
                                               datetime.datetime.now(),
                                               time_left)
                e_book_shared.sharer = self.owner
                if len(self.user_instance.requested_books) == 0:
                    self.user_instance.requested_books[self.isbn] = e_book_shared
                else:
                    occurrences = False
                    for book_isbn_key in self.user_instance.rented_books.keys():
                        if self.book_instance.isbn == book_isbn_key:
                            QtGui.QMessageBox.about(self, "Error", "Book already owned by User: " +
                                                    self.user_instance.username)
                            occurrences = True
                            break
                    if not occurrences:
                        self.user_instance.requested_books[self.isbn] = e_book_shared
            update_serialized_user(self.user_instance)
            update_serialized_user(self.owner_instance)
            self.main_window.reload_user_info()
        self.hide()


class ShareRequestFormView(QtGui.QWidget):
    def __init__(self, model, main_window, user_instance):
        self.model = model
        self.main_window = main_window
        self.user_instance = user_instance
        self.owner_instance = None
        self.book = None
        self.requested_book = None
        super(ShareRequestFormView, self).__init__()
        self.ui = Ui_ShareRequestWidget.Ui_Form()
        self.build_ui()
        self.load_requested_books()

    def build_ui(self):
        self.ui.setupUi(self)

        self.ui.accept_push_button.clicked.connect(lambda: self.accept(
            self.ui.share_request_table_widget.selectedItems()))
        self.ui.decline_push_button.clicked.connect(lambda: self.decline(
            self.ui.share_request_table_widget.selectedItems()))

    def accept(self, row_items):
        self.book = self.model.get_book_instance(row_items[2].text())
        self.requested_book = self.user_instance.requested_books[self.book.isbn]
        self.owner_instance = load_serialized_user(self.requested_book.sharer)
        # check if user has enough credits
        total_cost = self.book.price * self.requested_book.length_on_rent
        # Checks if the User has enough credits to receive the book
        if total_cost > self.user_instance.credits:
            QtGui.QMessageBox.about(self, "Error", "You do not have enough credits. You need " + str(total_cost) +
                                    " credits")
        else:
            # Checks if owner has enough time left
            if self.requested_book.length_on_rent > self.owner_instance.rented_books[self.book.isbn].length_on_rent:
                QtGui.QMessageBox.about(self, "Error", "User: " + self.owner_instance.username +
                                        " does not have enough time to share this book anymore")
                del self.user_instance.requested_books[self.requested_book.isbn]
            else:
                # decrement credits from user and increment credits to the person sharing
                self.user_instance.credits -= total_cost
                self.owner_instance.credits += total_cost
                self.owner_instance.rented_books[self.book.isbn].length_on_rent -= self.requested_book.length_on_rent
                # add book to rented book list
                self.user_instance.rented_books[self.book.isbn] = self.requested_book
                # remove book from requested book list
                # self.requested_book = None
                del self.user_instance.requested_books[self.requested_book.isbn]
            update_serialized_user(self.user_instance)
            update_serialized_user(self.owner_instance)
            self.load_requested_books()
            self.main_window.reload_user_info()

    def decline(self, row_items):
        self.book = self.model.get_book_instance(row_items[2].text())
        self.requested_book = self.user_instance.requested_books[self.book.isbn]
        # remove book from requested book list
        del self.user_instance.requested_books[self.requested_book.isbn]
        update_serialized_user(self.user_instance)
        self.load_requested_books()
        self.main_window.reload_user_info()
        # self.user_instance.requested_books[self.model.get_book_instance(row_items[2].text()).isbn] = None

    def load_requested_books(self):
        self.ui.share_request_table_widget.setRowCount(0)
        row = 0
        requested_books_instances = []
        if len(self.user_instance.requested_books) > 0:
            self.user_instance = load_serialized_user(self.user_instance.username)
            for purchased_ebook in self.user_instance.requested_books.values():
                requested_books_instances.append(purchased_ebook)
        for purchased_ebook in requested_books_instances:
            self.owner_instance = load_serialized_user(purchased_ebook.sharer)
            ebook = load_serialized_ebook(purchased_ebook.isbn)
            total_cost = ebook.price * purchased_ebook.length_on_rent
            self.ui.share_request_table_widget.insertRow(row)
            self.ui.share_request_table_widget.setItem(row, 0,
                                                       QtGui.QTableWidgetItem(ebook.title))
            self.ui.share_request_table_widget.setItem(row, 1,
                                                       QtGui.QTableWidgetItem(ebook.author))
            self.ui.share_request_table_widget.setItem(row, 2,
                                                       QtGui.QTableWidgetItem(ebook.isbn))
            self.ui.share_request_table_widget.setItem(row, 3,
                                                       QtGui.QTableWidgetItem(str(ebook.price)))
            self.ui.share_request_table_widget.setItem(row, 4,
                                                       QtGui.QTableWidgetItem(ebook.uploader.username))
            self.ui.share_request_table_widget.setItem(row, 5,
                                                       QtGui.QTableWidgetItem(str(ebook.rating)))
            self.ui.share_request_table_widget.setItem(row, 6,
                                                       QtGui.QTableWidgetItem(str(purchased_ebook.length_on_rent)))
            self.ui.share_request_table_widget.setItem(row, 7,
                                                       QtGui.QTableWidgetItem(str(total_cost)))
            self.ui.share_request_table_widget.setItem(row, 8,
                                                       QtGui.QTableWidgetItem(purchased_ebook.sharer))
            row += 1
