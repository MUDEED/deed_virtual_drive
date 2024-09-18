import os
import ctypes
import string
import subprocess


ASCII_LETTERS = string.ascii_uppercase


def get_unavailable_drives() -> list[str]:
    drive_bit = ctypes.windll.kernel32.GetLogicalDrives()
    drive_letter_list = []
    for letter in ASCII_LETTERS:
        if drive_bit & 1:
            drive_letter_list.append(letter)
        drive_bit >>= 1

    return drive_letter_list


def get_available_drives() -> list[str]:

    used_drive = get_unavailable_drives()
    all_letters = list(ASCII_LETTERS)

    return sorted(list(set(all_letters) - set(used_drive)))


def subst_drive(drive_letter="", path="", remove=False):

    if remove:
        proc = subprocess.run(
            ["subst", "/D", drive_letter], capture_output=True, check=False
        )

    else:
        proc = subprocess.run(
            ["subst", drive_letter, path], capture_output=True, check=False
        )

    if any((proc.stdout, proc.stderr)):
        return (proc.stdout, proc.stderr)

    return None


def get_subst_drive_dict():

    proc = subprocess.Popen(
        "chcp 65001 | subst",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=os.environ,
        shell=True,
        encoding="utf-8",
    )
    stdout, _ = proc.communicate()
    drive_dict = {}
    if stdout:
        for line in stdout.split("\n"):
            if line:
                drive_letter, v_path = line.rsplit(" => ", maxsplit=1)
                drive_dict.setdefault(drive_letter.replace("\\:", ""), v_path)

    return drive_dict
