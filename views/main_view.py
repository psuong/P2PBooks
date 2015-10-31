from PySide import QtGui, QtWebKit, QtCore
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

    def build_ui(self):
        self.ui.setupUi(self)

        # Disable line edits
        self.ui.published_by_line_edit.setDisabled(True)
        self.ui.ratings_line_edit.setDisabled(True)
        self.ui.title_line_edit.setDisabled(True)

        # Connect buttons
        self.ui.read_pause_push_button.clicked.connect(self.read_pause)
        self.ui.share_push_button.clicked.connect(self.share)
        self.ui.report_push_button.clicked.connect(self.report)

        self.ui.web_view.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        self.ui.web_view.show()
        self.ui.web_view.load(QtCore.QUrl('file:///C:/Users/unid/OneDrive/p2pbooks/views/pdf.pdf'))

    def read_pause(self):
        if self.ui.read_pause_push_button.text():
            # Pause the book
            self.model.pause_book()
        else:
            # Check if book can be read
            self.model.read_book()

    def share(self):
        pass

    def report(self):
        pass
