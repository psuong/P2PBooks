import sys
from PySide import QtGui
from views.main_view import UploadFormView, MainWindowVisitorView, ReaderFormView, MainWindowRegisteredView


class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_view = MainWindowRegisteredView(None)
        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
