# !/usr/bin/env python3
import sys

import yapom.utils as utils

from pathlib import Path
from yapom.utils import pomtext

USER_BIN_FOLDERS = ["~/.local/bin", "~/.local/share/bin", "~/.local/lib/bin"]


def determine_user_bin_folder() -> Path | None:
    # Find the first existing target directory
    for candidate in USER_BIN_FOLDERS:
        path = Path(candidate).expanduser().absolute()
        if path.exists():
            return path
    return None


def check_notify_send_installation():
    print(pomtext("Checking if 'notify-send' is installed ..."))
    if not utils.is_notify_send_installed():
        print("[ERROR] 'notify-send' not found!")
        sys.exit("Please make sure 'libnotify-bin' is installed.")
    print(pomtext("'notify-send' found!"))


def check_tcl_installation():
    print(pomtext("Checking if Tcl / Tk is installed ..."))
    if not utils.is_tcl_installed():
        print("[ERROR] tclsh not found - Tcl / Tk may not be installed (properly).")
        sys.exit(
            "Please ensure Tcl was installed properly: https://tkdocs.com/tutorial/install.html"
        )
    print(pomtext("Tcl found!"))


def create_symlink_in_user_bin(user_bin: Path):
    print(f"Creating symlink from (yapom) main.py to {target_dir}")
    symlink_path = Path(target_dir) / "yapom"
    main_py_path = Path("main.py").absolute()

    # Remove existing symlink if it exists
    if symlink_path.exists():
        symlink_path.unlink()

    # Create the new symlink
    symlink_path.symlink_to(main_py_path)
    print(f"Symlink created: {symlink_path} -> {main_py_path}")


print(pomtext("Installation process started ..."))

check_notify_send_installation()
check_tcl_installation()

print(f"Creating yapom HOME directory: {utils.HOME_DIR}")
utils.home_dir()

if not (target_dir := determine_user_bin_folder()):
    print("User /bin folder not found!")
    print(f"Checked the following locations: {', '.join(USER_BIN_FOLDERS)}")
    sys.exit(1)
create_symlink_in_user_bin(user_bin=target_dir)

print(pomtext("yapom installation finished!"))
print(pomtext("Please make sure that yapom/main.py is executable:"))
print(pomtext("  $ cd yapom"))
print(pomtext("  $ chmod +x main.py"))
