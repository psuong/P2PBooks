from PySide import QtGui, QtCore
from datetime import datetime
from ui import Ui_UploadForm, Ui_ReaderForm, Ui_ReportDialog, Ui_LoginForm, Ui_RegisterForm, Ui_MainWindowVisitor, \
    Ui_MainWindowRegistered, Ui_ConfirmPurchaseDialog, Ui_ApprovalReportedList
from models.main_model import submit_upload_form
from database.database_objects import load_serialized_user
import os


class UploadFormView(QtGui.QWidget):
    def __init__(self, model, username, main_window_inst):
        self.model = model
        super(UploadFormView, self).__init__()
        self.ui = Ui_UploadForm.Ui_Form()
        self.build_ui()
        self.file_location = None
        self.main_window = main_window_inst
        self.username = username

    def build_ui(self):
        self.ui.setupUi(self)
        # Disable text edit and also put a temporary message
        # self.ui.preview_text_edit.setText('Please click upload to show preview.')
        # self.ui.preview_text_edit.setDisabled(True)

        # Connect buttons to functions
        self.ui.upload_push_button.clicked.connect(self.upload)
        self.ui.submit_push_button.clicked.connect(self.submit)

    def upload(self):
        file_location = QtGui.QFileDialog.getOpenFileName(self, 'Open eBook', '', 'eBook Formats (*.pdf *.txt)')
        self.file_location = file_location[0]
        if self.file_location:
            self.ui.file_location_label.setText("File: " + self.file_location)

    def submit(self):
        # Make sure all fields are entered before submitting
        if self.ui.title_line_edit.text() and self.ui.author_line_edit.text() and self.ui.genres_line_edit.text() \
                and self.ui.isbn_line_edit.text():
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
                                   self.ui.cover_img_line_edit.text(),
                                   self.file_location
                                   )
                self.main_window = MainWindowRegisteredView(self.model, self.username)
                self.main_window.show()
                self.close()
            else:
                # Returns an Error message if file DNE
                QtGui.QMessageBox.about(self, "Invalid PDF", "PDF file does not exist: " + str(self.file_location))
        else:
            QtGui.QMessageBox.about(self, "Error", "Invalid Fields.")
    
    def closeEvent(self, *args, **kwargs):
        self.main_window.show()
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

    def build_ui(self):
        self.ui.setupUi(self)

        self.ui.summary_text_browser.setText(self.summary)
        self.ui.cover_img_web_view.setHtml('<img alt="Cover img" '
                                           'src="' + self.cover_img + '" style="width: 300px; height: 300px">')
        self.ui.cost_label.setText(str(self.rate))

    def accept(self, *args, **kwargs):
        pass

    def reject(self, *args, **kwargs):
        self.main_window.show()
        super(ConfirmedPurchaseDialogView, self).reject()


class ReportDialogView(QtGui.QDialog):
    def __init__(self, model):
        self.model = model
        super(ReportDialogView, self).__init__()
        self.ui = Ui_ReportDialog.Ui_Dialog()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Give reason options to report_combo_box
        self.ui.report_combo_box.addItems(["",
                                           "Violent/repulsive content",
                                           "Spam/misleading",
                                           "Copyright violation infringement",
                                           "None of the above (Specify below)",
                                           ])

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
                self.close()
        else:
            # Display an error message to tell the user to select a selection from the combo box
            QtGui.QMessageBox.about(self, "Error", "Please select a reason from the dropdown")


class ReaderFormView(QtGui.QWidget):
    def __init__(self, model, current_book):
        self.model = model
        super(ReaderFormView, self).__init__()
        self.ui = Ui_ReaderForm.Ui_Form()
        self.report_dialog = ReportDialogView(self.model)
        self.timer = QtCore.QTimer(self)
        self.paused = True
        self.location = None
        self.reader_process = None
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Disable line edits
        self.ui.published_by_line_edit.setDisabled(True)
        self.ui.ratings_line_edit.setDisabled(True)
        self.ui.title_line_edit.setDisabled(True)

        # Set book to paused state
        self.ui.read_pause_push_button.setText('Read')

        # TODO: Write function get the progression
        self.ui.progress_bar.setValue(50)

        # Connect buttons
        self.ui.read_pause_push_button.clicked.connect(self.read_pause)
        self.ui.share_push_button.clicked.connect(self.share)
        self.ui.report_push_button.clicked.connect(self.report)
        self.ui.browse_pdf_reader_push_button.clicked.connect(self.browse_reader_location)

        self.timer.timeout.connect(self.show_time)

    @QtCore.Slot()
    def show_time(self):
        self.ui.time_remaining_label.setText(datetime.now().strftime('%H:%M:%S %m/%d/%y'))

    @QtCore.Slot()
    def read_pause(self):
        if not self.paused:
            # Pause the book
            if self.model.pause_book():
                self.paused = True
                self.reader_process.kill()
                self.timer.stop()
        else:
            # Check if book can be read
            if self.model.read_book():
                arguments = ['C:/Users/unid/OneDrive/p2pbooks/views/pdf.pdf']
                self.reader_process = QtCore.QProcess(self)
                self.reader_process.started.connect(self.started)
                self.reader_process.finished.connect(self.finished)
                self.reader_process.start(self.location, arguments)
                self.paused = False

    @QtCore.Slot()
    def started(self):
        print datetime.now()
        self.ui.read_pause_push_button.setText('Pause')
        self.timer.start(1000)

    @QtCore.Slot()
    def finished(self):
        print datetime.now()
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
    def browse_reader_location(self):
        self.location = QtGui.QFileDialog.getOpenFileName(self, 'Open PDF Reader', '', 'PDF Reader Formats (*.exe)')
        if self.location[1]:
            self.ui.pdf_reader_path_label.setText(self.location[1])


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
                self.user_file = load_serialized_user(username)
                self.main_window = MainWindowRegisteredView(self.model, username, self.user_file.credits)
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
    def __init__(self, model, username, reputation):
        self.model = model
        self.purchase_dialog = None
        self.username = username
        self.reputation = reputation
        super(MainWindowRegisteredView, self).__init__()
        self.ui = Ui_MainWindowRegistered.Ui_MainWindow()
        self.upload_view = UploadFormView(self.model, username, self)
        self.user_file = load_serialized_user(self.username)
        self.build_ui()
        self.admin_view = None

    def build_ui(self):
        self.ui.setupUi(self)

        # Default text in Search Line Edit
        self.ui.search_line_edit.setPlaceholderText('Search...')

        # Hide results table widget for later
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()
        self.ui.library_table_widget.hide()

        self.ui.go_push_button.clicked.connect(self.search)
        self.ui.close_push_button.clicked.connect(self.close_search)
        self.ui.search_line_edit.returnPressed.connect(self.search)
        self.ui.upload_push_button.clicked.connect(self.upload)
        self.ui.library_push_button.clicked.connect(self.library)
        self.ui.admin_push_button.clicked.connect(self.admin)

        if self.user_file.group_policy == 'RU':
            self.ui.admin_push_button.hide()

        self.ui.username_label.setText('Hello ' + self.username)
        self.ui.reputation_label.setText('Credits: ' + str(self.reputation))

        self.load_ebooks()

        # Connect checkout buttons
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

    def close_search(self):
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()

    def upload(self):
        self.hide()
        self.upload_view.show()

    def library(self):
        if self.ui.library_table_widget.isHidden():
            self.ui.library_table_widget.show()
        else:
            self.ui.library_table_widget.hide()

    def admin(self):
        self.admin_view = ApprovalReportedMainView(self.model, self.username, self.reputation)
        self.admin_view.show()
        self.hide()


class ApprovalReportedMainView(QtGui.QWidget):
    def __init__(self, model, username, reputation):
        self.model = model
        self.username = username
        self.reputation = reputation
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
        self.main_view = MainWindowRegisteredView(self.model, self.username, self.reputation)
        self.main_view.show()
        self.hide()
