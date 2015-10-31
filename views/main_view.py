from PySide import QtGui
from ui import Ui_UploadForm, Ui_ReaderForm


class UploadFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(UploadFormView, self).__init__()
        self.ui = Ui_UploadForm.Ui_Form()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)
        # Disable text edit and also put a temporary message
        self.ui.preview_text_edit.setText('Please click upload to show preview.')
        self.ui.preview_text_edit.setDisabled(True)

        # Connect buttons to functions
        self.ui.upload_push_button.clicked.connect(self.upload)
        self.ui.submit_push_button.clicked.connect(self.submit)

    def upload(self):
        pass

    def submit(self):
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

        # Connect buttons
        self.ui.read_pause_push_button.clicked.connect(self.read_pause)
        self.ui.share_push_button.clicked.connect(self.share)
        self.ui.report_push_button.clicked.connect(self.report)

    def read_pause(self):
        if self.read_pause():
            # Pause the book
            pass
        else:
            # Check if book can be read
            pass

    def share(self):
        pass

    def report(self):
        pass
