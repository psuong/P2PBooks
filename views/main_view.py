from PySide import QtGui
from ui import Ui_UploadForm, Ui_RegisterForm


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
        self.ui.upload_push_button.clicked.connect(self.submit)

    def submit(self):
        self.ui.preview_text_edit.setText('P SUONG')


class RegisterFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(RegisterFormView, self).__init__()
        self.ui = Ui_RegisterForm.Ui_Form()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Connect buttons to functions
        self.ui.submit_push_button.clicked.connect(self.submit)

    def submit(self):
        pass
