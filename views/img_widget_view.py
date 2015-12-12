from PySide import QtGui, QtCore


class ImageWidget(QtGui.QWidget):
    """
    Image widget for TableWidget cells
    """

    def __init__(self, image_path, parent):
        super(ImageWidget, self).__init__(parent)
        self.image = QtGui.QPixmap(image_path)
        self.image = self.image.scaled(250,
                                       150,
                                       QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation)

    def paintEvent(self, *args, **kwargs):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(0, 0, self.image)
