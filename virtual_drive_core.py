import ctypes
import string
import os
import subprocess


def un_available_drives():
    drive_bit = ctypes.windll.kernel32.GetLogicalDrives()
    drive_letter_list = []
    for letter in string.ascii_uppercase:
        if drive_bit & 1:
            drive_letter_list.append(letter)
        drive_bit >>= 1

    return drive_letter_list


def available_drives():

    used = un_available_drives()
    all_letters = list(string.ascii_uppercase)

    return sorted(list(set(all_letters) - set(used)))


def subst_drive(drive_letter="", path="", remove=False):

    path = os.path.abspath(path)
    definde_dos_device = ctypes.windll.kernel32.DefineDosDeviceW

    if not remove:
        definde_dos_device.argtypes = [ctypes.c_int, ctypes.c_wchar_p, ctypes.c_wchar_p]
        if definde_dos_device(0, drive_letter, path) == 0:
            print("Subst failed on {}".format(path))
    else:
        definde_dos_device.argtypes = [ctypes.c_int, ctypes.c_wchar_p]
        if definde_dos_device(1, drive_letter) == 0:
            print("Couldn't remove subst {}".format(drive_letter))


def get_subst_drive_list():

    proc = subprocess.Popen(["subst"], stdout=subprocess.PIPE)
    stdout, _ = proc.communicate()
    drive_dict = {}
    if stdout:
        for line in stdout.decode("utf-8").split("\n"):
            if line:

                drive_letter, v_path = line.rsplit(" => ", maxsplit=1)

                drive_dict.setdefault(drive_letter.replace("\\:", ""), v_path)

    print(drive_dict)
    return drive_dict


if __name__ == "__main__":
    # subst_drive("X:", os.path.abspath("F:/Blender_Other_Project"))
    # subst_drive(drive_letter="T:", remove=True)
    get_subst_drive_list()
