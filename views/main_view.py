from PySide import QtGui, QtWebKit, QtCore
from datetime import datetime
import subprocess
from ui import Ui_UploadForm, Ui_ReaderForm


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


class ReaderFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(ReaderFormView, self).__init__()
        self.ui = Ui_ReaderForm.Ui_Form()
        self.build_ui()
        self.paused = True
        self.reader_process = None

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

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)

    def show_time(self):
        self.ui.time_remaining_label.setText(datetime.now().strftime('%H:%M:%S %m/%d/%y'))

    def read_pause(self):
        if not self.paused:
            # Pause the book
            if self.model.pause_book():
                self.paused = True
        else:
            # Check if book can be read
            if self.model.read_book():
                pdf_viewer = "C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe"
                arguments = ['C:/Users/unid/OneDrive/p2pbooks/views/pdf.pdf']
                reader_process = QtCore.QProcess(self)
                reader_process.started.connect(self.started)
                reader_process.finished.connect(self.finished)
                reader_process.start(pdf_viewer, arguments)

    def started(self):
        print datetime.now()
        self.ui.read_pause_push_button.setText('Pause')

    def finished(self):
        print datetime.now()
        self.ui.read_pause_push_button.setText('Read')

    def share(self):
        # Trigger the share widget
        pass

    def report(self):
        # Trigger the report widget
        pass
