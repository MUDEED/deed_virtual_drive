# -*- coding: utf-8 -*-
import os
import sys
from functools import partial

from Qt import QtCompat
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

from core import virtual_drive_core
from core import qt_utils
from widget import item_button
from widget import setting_widget

ROOT_PATH = os.path.dirname(__file__)
MAIN_UI_PATH = os.path.join(ROOT_PATH, "ui", "deed_virtual_drive.ui")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent=parent)
        QtCompat.loadUi(MAIN_UI_PATH, self)
        self.setWindowTitle("DEED Virtual Drive")
        qt_utils.dark_title_bar(self)

        reload_icon = QtGui.QPixmap(os.path.join(ROOT_PATH, "rsrc", "reload.png"))
        self.hdd_icon = QtGui.QPixmap(os.path.join(ROOT_PATH, "rsrc", "hdd.png"))

        self.setWindowIcon(self.hdd_icon)
        qt_utils.set_stylesheet(os.path.join(ROOT_PATH, "style", "bl_dark.qss"), self)

        self.comboBox.setView(QtWidgets.QListView())
        self.reload_btn.setText("")
        self.reload_btn.setIcon(QtGui.QIcon(reload_icon))

        self.comboBox.setCurrentIndex(0)
        self.settings = QtCore.QSettings(
            "deed_virtual_drive",
            "dvd_settings.ini",
        )

        self.lineEdit.textChanged.connect(self.line_edit_changed)

        self.lineEdit.setPlaceholderText("E.g. C:\\Program Files")
        self.pushButton.clicked.connect(self.add_drive)
        self.pushButton_2.clicked.connect(self.lineEdit.clear)
        self.toolButton.clicked.connect(self.set_directory_path)
        self.reload_btn.clicked.connect(self.update_drive)

        self.pushButton.setDisabled(True)
        self.actionAdd_drive.setDisabled(True)

        self.actionRefresh.triggered.connect(self.update_drive)
        self.actionAdd_drive.triggered.connect(self.add_drive)
        self.actionRemove_drive.triggered.connect(self.delete_drive)
        self.actionRemove_All.triggered.connect(self.delete_all_drive)
        self.actionSetting.triggered.connect(partial(self.open_setting_widget, self))

        if self.settings.value("auto_load") in qt_utils.TRUE_VALUE:
            self.load_drive_from_setting()
        self.update_drive()

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
                for drive_lt in virtual_drive_core.get_available_drives()
            ]
        )

        self.treeWidget.clear()

        drive_dict = virtual_drive_core.get_subst_drive_dict()
        print(drive_dict)
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

        img_path_list = (
            os.path.join(ROOT_PATH, "rsrc", "delete-button.png"),
            os.path.join(ROOT_PATH, "rsrc", "delete-button_hover.png"),
            os.path.join(ROOT_PATH, "rsrc", "delete-button_press"),
        )
        # remove button widget
        for items in item_list:
            item_btn = item_button.ItemButton(*img_path_list)
            item_btn.autoFillBackground()
            item_btn.setFixedSize(30, 30)
            item_btn.setToolTip("remove")

            item_btn.clicked.connect(partial(self.delete_drive, items))
            self.treeWidget.setItemWidget(items, 2, item_btn)

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

    def set_directory_path(self):
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

        qt_utils.dark_title_bar(message_box)
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
        _setting_widget = setting_widget.SettingWidget(parent)
        _setting_widget.exec()

        if _setting_widget.result():
            self.settings.setValue(
                "auto_load", _setting_widget.is_auto_load.isChecked()
            )
            self.settings.setValue(
                "auto_save", _setting_widget.is_auto_save_drive.isChecked()
            )

            self.save_setting_drive()
            self.settings.sync()

    def load_drive_from_setting(self):

        drive_dict = self.settings.value("drive_dict") or {}

        for drive_letter, drive_path in drive_dict.items():
            virtual_drive_core.subst_drive(
                drive_letter,
                drive_path,
            )

    def closeEvent(self, event):

        super(MainWindow, self).closeEvent(event)

        if self.settings.value("auto_save") in qt_utils.TRUE_VALUE:
            self.save_setting_drive()

    def save_setting_drive(self):
        drive_dict = {}
        for idx in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(idx)
            drive_dict[item.text(0)] = str(item.text(1))
            print(str(item.text(1)))

        self.settings.setValue("drive_dict", drive_dict)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()

    sys.exit(app.exec())
