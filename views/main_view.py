from PySide import QtGui, QtCore
from datetime import datetime
from ui import Ui_UploadForm, Ui_ReaderForm, Ui_ReportDialog, Ui_LoginForm, Ui_RegisterForm, Ui_MainWindowVisitor, Ui_MainWindowRegistered
from models.main_model import submit_upload_form


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
        self.model.upload_file(self.file_location)
        self.ui.file_location_label.setText("File: " + self.file_location)

    def submit(self):
        # Make sure all fields are entered before submitting
        if self.ui.title_line_edit.text() and self.ui.author_line_edit.text() and self.ui.genres_line_edit.text() \
                and self.ui.isbn_line_edit.text():
            upload_status = self.model.upload_status(self.file_location)
            if upload_status:
                # File uploaded successfully
                submit_upload_form(self.ui.title_line_edit.text(),
                                   self.ui.author_line_edit.text(),
                                   self.ui.genres_line_edit.text(),
                                   self.ui.isbn_line_edit.text(),
                                   self.ui.price_spin_box.text(),
                                   self.username,
                                   self.file_location
                                   )
                self.main_window = MainWindowRegisteredView(self.model, self.username)
                self.main_window.show()
                self.close()
            else:
                # Failure, return the error with second element in tuple of submit_status
                pass
    
    def closeEvent(self, *args, **kwargs):
        self.main_window.show()
        super(UploadFormView, self).closeEvent()


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
                QtGui.QMessageBox.about(self,"Error", "Please specify the reason in the description")
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
        if username == '' and password == '':
            # Must return a warning
            print "Empty Fields"
        else:
            # Check if the fields match a username and password is in the database
            if self.model.login_user(username, password) is not None:
                self.main_window = MainWindowRegisteredView(self.model, username)
                self.main_window.show()
                self.hide()
            else:
                # Nothing was return; error
                pass

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
        if password == confirm_password:
            self.model.register_user(username,
                                     password,
                                     self.ui.email_line_edit.text(),
                                     self.ui.dob_date_edit.date())
            self.registered_main_window = MainWindowRegisteredView(self.model,
                                                              self.ui.username_line_edit.text())
            self.registered_main_window.show()
            self.hide()
        else:
            # Throw a Warning
            pass


class MainWindowVisitorView(QtGui.QMainWindow):
    def __init__(self, model):
        self.model = model
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

    def search(self):
        if self.ui.search_line_edit.text():
            self.ui.search_table_widget.show()
            self.ui.close_push_button.show()

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
        self.username = username
        super(MainWindowRegisteredView, self).__init__()
        self.ui = Ui_MainWindowRegistered.Ui_MainWindow()
        self.upload_view = UploadFormView(self.model, username, self)
        self.build_ui()

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

        self.ui.username_label.setText(self.username)

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
