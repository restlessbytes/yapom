import re
import sys
import shutil
import subprocess

import tkinter as tk

from enum import Enum
from pathlib import Path


BG_DARK = "#2e2e2e"
# Tomato Emoji: https://emojipedia.org/tomato
TOMATO = "\U0001f345"
NOTIFY_TOOL = "notify-send"
# TODO HOME_DIR = "~/.yapom"
HOME_DIR = "dev_home/"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_RUNTIME = "25m"


class Status(Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    CANCELLED = "cancelled"
    FINISHED = "finished"


def pomtext(text: str) -> str:
    return f"( {TOMATO} ) {text}"


def home_dir() -> Path:
    if not (home_dir_path := Path(HOME_DIR).expanduser().absolute()).exists():
        home_dir_path.mkdir()
        print(pomtext(f"yapom HOME created: {home_dir_path}"))
    return home_dir_path


def no_session_in_progress_message(text: str) -> str:
    """
    Small "convenience" function that helps with messages of the form

      'No Pomodoro session in progress - nothing to cancel'

    etc.

    Returns a `pomtext` formatted message string.
    """
    return pomtext(f"No Pomodoro session in progress - {text}")


def is_installed(name: str) -> bool:
    return any(shutil.which(name) or "")


def format_runtime(seconds: int) -> str:
    """Convert seconds to 'h:m:s' format."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    result = ""
    if 0 < hours:
        result += str(hours) + "h"
    if 0 < minutes:
        result += str(minutes) + "m"
    if 0 < seconds:
        result += str(seconds) + "s"
    return result


def runtime_from_string(s: str) -> int:
    """
    Convert a "temporal" string of the form <H>h<M>m<S>s to an integer representing
    the runtime of that string in seconds.

    Example: "5m5s" = 305 (because 5 minutes and 5 seconds are 305 seconds in total)

    Strings that comprise a single integer are interpreted as 'seconds': "42" = 42.
    """
    try:
        return int(s)
    except ValueError:
        pass
    result = 0
    regex = re.compile(r"(\d+h)?(\d+m)?(\d+s)?")
    if match := regex.match(s.strip()):
        hours, minutes, seconds = match.groups()
        if hours:
            hours = int(hours.removesuffix("h")) * 3600
            result += hours
        if minutes:
            minutes = int(minutes.removesuffix("m")) * 60
            result += minutes
        if seconds:
            result += int(seconds.removesuffix("s"))
    return result


def time_elapsed_remaining_message(elapsed: int, remaining: int) -> str:
    elapsed_formatted = format_runtime(elapsed)
    remaining_formatted = format_runtime(remaining)
    return f"time elapsed: {elapsed_formatted}, time remaining: {remaining_formatted}"


def determine_runtime():
    try:
        return runtime_from_string(sys.argv[2].strip())
    except IndexError:
        return runtime_from_string(DEFAULT_RUNTIME)


def notify_user(message: str):
    try:
        # TODO Fails when used from within a virtual environment
        root = tk.Tk()
    except tk.TclError as tex:
        notify_send(message)
        sys.exit(pomtext(f"[WARNING][Tkinter] {tex}"))

    # Hide the main window
    root.withdraw()

    # Create a custom dialog window
    dialog = tk.Toplevel(root)
    dialog.title("Pomodoro Notification")
    dialog.resizable(False, False)
    dialog.geometry("300x150")
    dialog.configure(bg=BG_DARK)  # Dark background

    try:
        # Emojione - tomato Emoji - U+1F345
        # Source: https://commons.wikimedia.org/wiki/File:Emojione_1F345.svg
        # TODO Ensure that the image is still found under this 'relative' path!
        icon = tk.PhotoImage(
            file="resources/icons/Emojione_1F345_32px.svg.png"
        ).subsample(2, 2)
        dialog.iconphoto(False, icon)
        message_label = tk.Label(
            dialog,
            text=message,
            fg="white",
            bg=BG_DARK,
            padx=5,
            wraplength=280,
            image=icon,
            compound="left",
        )
    except Exception as e:
        print(pomtext(f"Could not load icon: {e}"))
        message_label = tk.Label(
            dialog, text=message, fg="white", bg=BG_DARK, wraplength=280
        )

    # Message label
    message_label.pack(pady=20)

    # OK button
    ok_button = tk.Button(
        dialog, text="OK", command=dialog.destroy, bg="#444444", fg="white"
    )
    ok_button.pack()

    dialog.mainloop()
    root.destroy()


def notify_send(message: str, do_exit: bool = True):
    if is_installed(NOTIFY_TOOL):
        try:
            subprocess.run([NOTIFY_TOOL, pomtext(message)], check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(pomtext(f"Notification failed: {e}"))
    else:
        sys.exit(
            pomtext(
                f"{NOTIFY_TOOL} not found. Please make sure libnotify-bin is installed."
            )
        )
