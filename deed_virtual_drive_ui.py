import os
import sys
from functools import partial
import ctypes

from Qt import QtCompat, QtWidgets, QtCore, QtGui

from core import virtual_drive_core

ROOT_PATH = os.path.dirname(__file__)
MAIN_UI_PATH = os.path.join(ROOT_PATH, "ui", "deed_virtual_drive.ui")
SETTING_UI_PATH = os.path.join(ROOT_PATH, "ui", "setting.ui")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent=parent)
        QtCompat.loadUi(MAIN_UI_PATH, self)
        self.setWindowTitle("DEED Virtual Drive")
        dark_title_bar(self)
        reload_icon = QtGui.QPixmap(os.path.join(ROOT_PATH, "rsrc", "reload.png"))
        self.hdd_icon = QtGui.QPixmap(os.path.join(ROOT_PATH, "rsrc", "hdd.png"))

        self.setWindowIcon(self.hdd_icon)
        self.setStyleSheet(open("style/bl_dark.qss", "r").read())
        self.comboBox.setView(QtWidgets.QListView())
        self.reload_btn.setText("")
        self.reload_btn.setIcon(QtGui.QIcon(reload_icon))
        self.update_drive()
        self.comboBox.setCurrentIndex(0)
        self.settings = QtCore.QSettings(
            os.path.join(
                os.path.expanduser("~"),
                "deed_virtual_drive",
                "dvd_settings.ini",
            ),
            QtCore.QSettings.IniFormat,
        )

        self.lineEdit.textChanged.connect(self.line_edit_changed)

        self.lineEdit.setPlaceholderText("E.g. C:\Program Files")
        self.pushButton.clicked.connect(self.add_drive)
        self.pushButton_2.clicked.connect(self.lineEdit.clear)
        self.toolButton.clicked.connect(self.directory_path)
        self.reload_btn.clicked.connect(self.update_drive)

        self.pushButton.setDisabled(True)
        self.actionAdd_drive.setDisabled(True)

        self.actionRefresh.triggered.connect(self.update_drive)
        self.actionAdd_drive.triggered.connect(self.add_drive)
        self.actionRemove_drive.triggered.connect(self.delete_drive)
        self.actionRemove_All.triggered.connect(self.delete_all_drive)
        self.actionSetting.triggered.connect(partial(self.open_setting_widget, self))

    def line_edit_changed(self):

        if not self.lineEdit.text or not os.path.exists(self.lineEdit.text()):
            self.pushButton.setDisabled(True)
            self.actionAdd_drive.setDisabled(True)
        else:
            self.actionAdd_drive.setEnabled(True)
            self.pushButton.setEnabled(True)

    def update_drive(self):
        self.comboBox.clear()
        self.comboBox.addItems(
            [
                "{}:".format(drive_lt)
                for drive_lt in virtual_drive_core.available_drives()
            ]
        )

        self.treeWidget.clear()

        drive_dict = virtual_drive_core.get_subst_drive_dict()
        item_list = []
        for drive_letter, drive_path in drive_dict.items():
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, drive_letter)
            item.setText(1, drive_path)
            item_list.append(item)

        self.treeWidget.addTopLevelItems(item_list)

        self.actionRemove_drive.setDisabled(True)
        self.actionRemove_All.setDisabled(True)
        if item_list:
            self.actionRemove_drive.setEnabled(True)
            self.actionRemove_All.setEnabled(True)

        for items in item_list:
            btn = QtWidgets.QPushButton("")
            btn.autoFillBackground()
            btn.setFixedSize(30, 30)
            btn.setToolTip("remove")
            btn.setStyleSheet(
                """
                * QPushButton{
                    border-image: url("rsrc/delete-button.png");
                    margin:2px;
                }
                * QPushButton:hover,
                * QPushButton:selected{
                    border-image: url("rsrc/delete-button_hover.png");                
                }
                * QPushButton:pressed{
                    border-image: url("rsrc/delete-button_press.png");
                }
            """
            )
            btn.clicked.connect(partial(self.delete_drive, items))
            self.treeWidget.setItemWidget(items, 2, btn)

        self.treeWidget.header().resizeSection(1, 500)
        self.treeWidget.resizeColumnToContents(2)

    def add_drive(self):

        if not (
            virtual_drive_core.subst_drive(
                self.comboBox.currentText(),
                os.path.realpath(self.lineEdit.text()),
            )
        ):
            self.lineEdit.clear()
            self.update_drive()

    def directory_path(self):
        exist_dir = QtWidgets.QFileDialog.getExistingDirectory()
        if exist_dir:
            self.lineEdit.setText(exist_dir)

    def delete_drive(self, item=None):

        if not item:
            item_list = self.treeWidget.selectedItems()

            if not item_list:
                self.show_message(
                    "Please select a Drive item in table",
                    "Please select a Drive",
                )
                return
            item = item_list[0]

        virtual_drive_core.subst_drive(item.text(0), remove=True)
        self.update_drive()

    def delete_all_drive(self):

        for index in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(index)
            virtual_drive_core.subst_drive(item.text(0), remove=True)

        self.update_drive()

    def show_message(self, text="", title=" "):

        message_box = QtWidgets.QMessageBox(parent=self)

        dark_title_bar(message_box)
        message_box.setText(text)
        message_box.setWindowTitle(title)

        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )
        message_box.exec_()

    def open_setting_widget(self, parent=None):
        self.setting_widget = SettingWidget(parent)
        self.setting_widget.exec_()
        if self.setting_widget.result():
            self.settings.setValue(
                "auto_load", self.setting_widget.is_auto_load.isChecked()
            )
            self.settings.setValue(
                "auto_save", self.setting_widget.is_auto_save_drive.isChecked()
            )
            self.settings.setValue(
                "load_startup", self.setting_widget.is_load_startup.isChecked()
            )


class SettingWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)
        QtCompat.loadUi(SETTING_UI_PATH, self)
        dark_title_bar(self)
        self.setWindowTitle("settings")
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )
        true_value = (True, "True", "true")
        self.is_auto_load.setChecked(
            True if parent.settings.value("auto_load") in true_value else False
        )
        self.is_auto_save_drive.setChecked(
            True if parent.settings.value("auto_save") in true_value else False
        )
        self.is_load_startup.setChecked(
            True if parent.settings.value("load_startup") in true_value else False
        )

        geo = self.geometry()
        geo.moveCenter(parent.geometry().center())
        self.setGeometry(geo)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.isDefault()
        self.ok_button.clicked.connect(self.accept)

        self.True_name()

    def True_name(self):
        print("test")


def dark_title_bar(widget=None):
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """

    dwmwa_use_immersive_dark_mode = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    # get_parent = ctypes.windll.user32.GetParent
    # hwnd = widget.winId() if widget else self.winId()
    hwnd = widget.winId()
    value = ctypes.c_int(1)
    set_window_attribute(
        hwnd,
        dwmwa_use_immersive_dark_mode,
        ctypes.byref(value),
        ctypes.sizeof(value),
    )


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.show()

    sys.exit(app.exec_())
