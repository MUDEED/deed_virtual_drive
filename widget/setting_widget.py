import os

from Qt import QtWidgets
from Qt import QtCore
from Qt import QtCompat

from core import qt_utils

SETTING_UI_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "ui", "setting.ui")
)


class SettingWidget(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)
        QtCompat.loadUi(SETTING_UI_PATH, self)
        qt_utils.dark_title_bar(self)

        self._parent = parent

        self.setWindowTitle("settings")
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )

        self.is_auto_load.setChecked(
            self._parent.settings.value("auto_load") in qt_utils.TRUE_VALUE
        )
        self.is_auto_save_drive.setChecked(
            self._parent.settings.value("auto_save") in qt_utils.TRUE_VALUE
        )

        setting_geo = self.geometry()
        setting_geo.moveCenter(self._parent.geometry().center())
        self.setGeometry(setting_geo)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.isDefault()
        self.ok_button.clicked.connect(self.accept)
