from PySide import QtGui
from ui import Ui_UploadForm, Ui_LoginForm


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

class LoginFormView(QtGui.QWidget):
    def __init__(self, model):
        self.model = model
        super(LoginFormView, self).__init__()
        self.ui = Ui_LoginForm.Ui_Form()
        self.build_ui()

    def build_ui(self):
        self.ui.setupUi(self)
        # Connect buttons to login
        self.ui.login_push_button.clicked.connect(self.login)
        self.ui.guest_session_push_button.connect(self.guest_session)
        self.ui.sign_up_push_button.connect(self.register)

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

    def guest_session(self):
        # Function must open up the home window
        pass

    def register(self):
        # Function must open up the Register window
        pass
