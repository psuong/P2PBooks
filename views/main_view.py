from PySide import QtGui
from ui import Ui_UploadForm, Ui_ReportDialog


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


class ReportDialogView(QtGui.QDialog):
    def __init__(self, model):
        self.model = model
        super(ReportDialogView, self).__init__()
        self.ui = Ui_ReportDialog.Ui_Dialog()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)

        # Give reason options to report_combo_box
        self.ui.report_combo_box.addItems(["Violent or repulsive content", "Spam or misleading", "Copyright infringement"])

        # Connect button Ok button to function
        self.ui.report_button_box.clicked.connect(self.submit)

    def submit(self):
        self.ui.report_text_edit.setText("IT WORKS")
