import ctypes
from Qt import QtWidgets

TRUE_VALUE = (True, "True", "true")


def set_stylesheet(qss_file: str, widget: QtWidgets.QWidget):

    with open(qss_file, "r") as f_style:
        widget.setStyleSheet(f_style.read())


def dark_title_bar(widget=None):
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """

    dwmwa_use_immersive_dark_mode = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute

    hwnd = widget.winId()
    value = ctypes.c_int(1)
    set_window_attribute(
        hwnd,
        dwmwa_use_immersive_dark_mode,
        ctypes.byref(value),
        ctypes.sizeof(value),
    )
