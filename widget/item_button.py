from Qt import QtWidgets
from Qt import QtGui


class ItemButton(QtWidgets.QToolButton):

    def __init__(self, image_path, hover_path=None, press_path=None):
        super(ItemButton, self).__init__()

        self.image_pixmap = QtGui.QPixmap(image_path)
        self.hover_pixmap = QtGui.QPixmap(hover_path) if hover_path else None
        self.press_pixmap = QtGui.QPixmap(press_path) if press_path else None

        self.pixmap = self.image_pixmap

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def enterEvent(self, event):
        self.pixmap = self.hover_pixmap
        self.update()

    def leaveEvent(self, event):
        self.pixmap = self.image_pixmap
        self.update()

    def mousePressEvent(self, event):
        super(ItemButton, self).mousePressEvent(event)
        self.pixmap = self.image_pixmap

        self.update()
