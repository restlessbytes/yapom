import sys

import yapom.utils as utils
import yapom.pomodoro as pomodoro

from os import getpid
from time import sleep
from datetime import datetime


if __name__ == "__main__":
    pid = getpid()
    try:
        runtime = int(sys.argv[1])
        sleep(runtime)
    except Exception as ex:
        error_message = pomodoro.pomtext(f"Pomodoro session failed: {ex} (pid={pid})")
        sys.exit(error_message)
    try:
        pomodoro.finish(end_time=datetime.now())
    except ValueError:
        sys.exit(f"No such PID in pomodoro sessions file: {pid}")
    # utils.notify_send("Pomodoro session finished!")
    utils.notify_user("Pomodoro session finished!")
