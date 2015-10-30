from PySide import QtGui
from ui import Ui_UploadForm


class UploadFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(UploadFormView, self).__init__()
        self.build_ui()
        self.ui = Ui_UploadForm.Ui_Form()

    def build_ui(self):
        self.ui.setupUi(self)
