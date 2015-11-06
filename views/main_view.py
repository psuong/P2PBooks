from PySide import QtGui, QtCore
from datetime import datetime
from ui import Ui_UploadForm, Ui_ReaderForm, Ui_ReportDialog, Ui_LoginForm, Ui_MainWindowVisitor


class UploadFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(UploadFormView, self).__init__()
        self.ui = Ui_UploadForm.Ui_Form()
        self.build_ui()
        self.file_location = None

    def build_ui(self):
        self.ui.setupUi(self)
        # Disable text edit and also put a temporary message
        self.ui.preview_text_edit.setText('Please click upload to show preview.')
        self.ui.preview_text_edit.setDisabled(True)

        # Connect buttons to functions
        self.ui.upload_push_button.clicked.connect(self.upload)
        self.ui.submit_push_button.clicked.connect(self.submit)

    def upload(self):
        # Make sure all fields are entered
        if self.ui.title_line_edit.text() and self.ui.author_line_edit.text() and self.ui.genres_line_edit.text() \
                and self.ui.isbn_line_edit.text():
            file_location = QtGui.QFileDialog.getOpenFileName(self, 'Open eBook', '', 'eBook Formats (*.pdf *.txt)')
            self.file_location = file_location[0]
            self.model.upload_file(self.file_location)

    def submit(self):
        submit_status = self.model.submit_file(self.file_location)
        if submit_status[0]:
            # File uploaded successfully
            pass
        else:
            # Failure, return the error with second element in tuple of submit_status
            pass


class ReportDialogView(QtGui.QDialog):
    def __init__(self, model):
        self.model = model
        super(ReportDialogView, self).__init__()
        self.ui = Ui_ReportDialog.Ui_Dialog()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Give reason options to report_combo_box
        self.ui.report_combo_box.addItems(["Violent or repulsive content",
                                           "Spam or misleading",
                                           "Copyright infringement"])

        # Connect button Ok button to function
        self.ui.report_button_box.clicked.connect(self.accept)

    def accept(self, *args, **kwargs):
        # Press OK
        pass

    def reject(self, *args, **kwargs):
        # Press Cancel
        pass


class ReaderFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(ReaderFormView, self).__init__()
        self.ui = Ui_ReaderForm.Ui_Form()
        self.report_dialog = ReportDialogView(self.model)
        self.timer = QtCore.QTimer(self)
        self.paused = True
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
                pdf_viewer = "C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe"
                arguments = ['C:/Users/unid/OneDrive/p2pbooks/views/pdf.pdf']
                self.reader_process = QtCore.QProcess(self)
                self.reader_process.started.connect(self.started)
                self.reader_process.finished.connect(self.finished)
                self.reader_process.start(pdf_viewer, arguments)
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


class MainWindowVisitorView(QtGui.QMainWindow):
    def __init__(self, model):
        self.model = model
        super(MainWindowVisitorView, self).__init__()
        self.ui = Ui_MainWindowVisitor.Ui_MainWindow()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Hide results table widget for later
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()

        self.ui.go_push_button.clicked.connect(self.search)
        self.ui.close_push_button.clicked.connect(self.close_search)

    def search(self):
        self.ui.search_table_widget.show()
        self.ui.close_push_button.show()

    def close_search(self):
        self.ui.search_table_widget.hide()
        self.ui.close_push_button.hide()


class LoginFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(LoginFormView, self).__init__()
        self.ui = Ui_LoginForm.Ui_Form()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)
        # Connect buttons to their respective functions
        self.ui.login_push_button.clicked.connect(self.login)
        self.ui.sign_up_push_button.clicked.connect(self.sign_up)

    def login(self):
        # Grab component in object
        username = self.ui.username_line_edit.text()
        password = self.ui.password_line_edit.text()
        if username == '' and password == '':
            # Must return a warning
            print "Empty Fields"
        else:
            # Check if the fields match a username and password is in the database
            print "Non-Empty Fields"

    # sign_up(self) must open up the Register window
    def sign_up(self):
        pass
