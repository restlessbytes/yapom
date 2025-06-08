import os
import json
import signal
import subprocess

import yapom.utils as utils

from pathlib import Path
from datetime import datetime

from yapom.utils import Status, DATETIME_FORMAT


def get_filepath() -> Path:
    if not (session_file := utils.home_dir() / Path(".session")).exists():
        session_file.touch()
    return session_file


def read() -> dict:
    with get_filepath().open("r") as session_file:
        try:
            return json.load(session_file)
        except json.decoder.JSONDecodeError:
            return {}


def write(data: dict) -> dict:
    current_session_file = read()
    current_session_file.update(data)
    with get_filepath().open(mode="w+") as session_file:
        json.dump(obj=current_session_file, fp=session_file)
        return current_session_file


def update(data: dict) -> dict:
    current = read()
    current.update(data)
    write(current)
    return current


def get_current_status() -> Status | None:
    """
    Get the status of the current (or latest) Pomodoro session.
    """
    if current_status := read().get("status"):
        return Status(current_status)
    return None


def is_running() -> bool:
    return get_current_status() == Status.RUNNING


def is_in_progress() -> bool:
    return get_current_status() in {Status.STOPPED, Status.RUNNING}


def has_finished() -> bool:
    return get_current_status() in {Status.FINISHED, Status.CANCELLED}


def get_runtimes() -> tuple[int, int] | None:
    if has_finished():
        return None
    data = read()
    start_time_str = data["start"]
    original_runtime = data["runtime"]
    if time_ref := data.get("stop"):
        time_ref = datetime.strptime(time_ref, DATETIME_FORMAT)
    else:
        time_ref = datetime.now()

    start_time = datetime.strptime(start_time_str, DATETIME_FORMAT)

    # Calculate elapsed time and remaining runtime
    time_elapsed = int((time_ref - start_time).total_seconds())
    remaining_runtime = int(original_runtime - time_elapsed)

    return time_elapsed, remaining_runtime


def start_timer(runtime: int) -> tuple[int, datetime]:
    """
    Start a new Pomodoro timer for the current session.

    Returns PID and start time (as `datetime`) for the timer process.
    """
    process = subprocess.Popen(f"python3 pomtimer.py {runtime}".split())
    return process.pid, datetime.now()


def kill_current() -> int | None:
    """
    (Try to) Kill the currently running pomodoro process (i.e. 'python3 session.py').

    If successful, return the PID of this process; if no such process exists at the
    moment, return `None`.
    """
    try:
        pid = read()["pid"]
        os.kill(pid, signal.SIGKILL)
        return pid
    except ProcessLookupError:
        return None
