import sys

import yapom.utils as utils
import yapom.history as history
import yapom.session as session

from datetime import datetime

from yapom.utils import Status, pomtext


def status() -> str:
    """
    Return a string describing the 'state' of the current (or 'latest') Pomodoro session.

    This function returns a 'pomtext' string.
    """
    if latest := session.read():
        # start_time, end_time, runtime, latest_status = latest
        runtime = int(latest["runtime"])
        runtime_fmt = utils.format_runtime(runtime) or "-"
        latest_status = Status(latest["status"]).name
        start_time = latest["start"]
        day_start, start_time = start_time.split()
        if end_time := latest.get("end"):
            day_end, end_time = end_time.split()
            if day_start == day_end:
                message = f"{latest_status} ({runtime_fmt}) (from {start_time} to {end_time}) [{day_start}]"
            else:
                message = (
                    f"[{day_start}:{start_time}] [{day_end}:{end_time}] {latest_status}"
                )
        else:
            message = (
                f"{latest_status} ({runtime_fmt}) (from {start_time}) [{day_start}]"
            )
    else:
        message = "No Pomodoro session found."
    return pomtext(message)


def start(runtime: int) -> str:
    if session.is_in_progress():
        return pomtext("A Pomodoro session is already in progress.")
    pid, start_time = session.start_timer(runtime=runtime)
    session_data = {
        "pid": pid,
        "start": start_time.strftime(utils.DATETIME_FORMAT),
        "stop": "",
        "end": "",
        "runtime": runtime,
        "status": Status.RUNNING.value,
    }
    session.write(session_data)
    return status()


def stop() -> str:
    """
    Stop or pause the current Pomodoro session.

    The session can be resumed later.
    """
    if session.has_finished():
        return utils.no_session_in_progress_message("nothing to stop.")
    if session.is_running():
        session.kill_current()
        stopped_data = {
            "pid": "",
            "stop": datetime.now().strftime(utils.DATETIME_FORMAT),
            "status": Status.STOPPED.value,
        }
        session.update(stopped_data)
        elapsed, remaining = session.get_runtimes()
        print(
            utils.pomtext(
                f"Session stopped - ({utils.time_elapsed_remaining_message(elapsed=elapsed, remaining=remaining)})"
            )
        )
    # If session has already been stopped, this would just echo the current 'stopped' status.
    return status()


def resume():
    """
    Resume a stopped Pomodoro session.
    """
    if session.has_finished():
        return utils.no_session_in_progress_message("nothing to resume.")
    if session.is_running():
        # 'Resuming' an already running session shouldn't do anything.
        return status()

    elapsed, remaining = session.get_runtimes()

    # Start the timer again with the remaining runtime
    # (NOTE start_time stays the same!)
    pid, _ = session.start_timer(remaining)
    session.update(
        {
            "pid": pid,
            "status": Status.RUNNING.value,
            # Remove the 'stop' field by setting it to an empty string
            "stop": "",
        }
    )
    print(
        utils.pomtext(
            f"Session restarted - ({utils.time_elapsed_remaining_message(elapsed=elapsed, remaining=remaining)})"
        )
    )
    return status()


def finish(end_time: datetime, with_status: Status = Status.FINISHED) -> Status:
    """
    Finish pomodoro session (either because time is up or it has been cancelled).
    """
    # Update session file
    end_str = end_time.strftime(utils.DATETIME_FORMAT)
    updated = session.update({"stop": "", "end": end_str, "status": with_status.value})
    history.archive_pomodoro_session(updated)
    return with_status


def cancel() -> str:
    """
    Cancel the current Pomodoro session if it hasn't finished.
    """
    if session.has_finished():
        return utils.no_session_in_progress_message("nothing to cancel.")
    try:
        session.kill_current()
        finish(end_time=datetime.now(), with_status=Status.CANCELLED)
        return status()
    except Exception as ex:
        sys.exit(f"Failed to cancel current Pomodoro session: {ex}")


def reset() -> str:
    """
    Reset the start date of the current session to 'now' and then restart it.
    """
    if session.has_finished():
        return utils.no_session_in_progress_message("nothing to reset / restart")
    session.kill_current()
    updated = session.update({"status": Status.CANCELLED.value})
    return start(int(updated["runtime"]))


def repeat() -> str:
    """
    Run the last Pomodoro session again with the same runtime.
    """
    if session.is_in_progress():
        return utils.pomtext(
            "Can't repeat last session because it's still in progress."
        )
    last_runtime = int(session.read()["runtime"])
    return start(runtime=last_runtime)
