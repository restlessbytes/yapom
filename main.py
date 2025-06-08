# !/usr/bin/env python3

import sys

import yapom.pomodoro as pomodoro
import yapom.utils as utils


HELP = """Usage: yapom [COMMAND]

Manage Pomodoro sessions from the comforts of the command line.

Commands:                                                                                    
  help             Display this help message
  status           Show status of current (or last) Pomodoro session
  start [TIME|NUM] Start a new Pomodoro session (NUM is interpreted as 'seconds')
  stop             Stop the current session (same as 'pause')
  pause            Pause the current session (same as 'stop')
  resume           Resume a paused (or stopped) session
  cancel           Cancel the current session
  reset            Reset the current session (same as 'restart')
  restart          Restart the current session (same as 'reset')
  repeat           Repeat the last session (i.e. new session, same runtime)
  report           Generate a report about your Pomodoro history
  tomato           Print tomato emoji
                                                          
Time format: [HOURS]h[MINUTES]m[SECONDS]s
  * At least one must be specified
  * A single integer without (h|m|s) is interpreted as "seconds"

Examples:
  1h5m10s = 1 hour, 5 minutes, 10 seconds
  1h42s   = 1 hour, 42 seconds
  25m     = 25 minutes (default length for Pomodoro sessions btw)
  5       = 5 seconds
"""


def main():
    command = sys.argv[1]

    match command:
        case "help":
            print(HELP)
        case "status":
            print(pomodoro.status())
        case "start":
            runtime = utils.determine_runtime()
            print(pomodoro.start(runtime))
        case "stop" | "pause":
            print(pomodoro.stop())
        case "resume":
            print(pomodoro.resume())
        case "cancel":
            print(pomodoro.cancel())
        case "reset" | "restart":
            print(pomodoro.reset())
        case "repeat":
            print(pomodoro.repeat())
        case "report":
            # TODO
            print("This feature hasn't been implemented yet!")
        case "tomato" | "pomodoro":
            print(utils.TOMATO)
        case _:
            sys.exit(f"Unknown command: '{command}'")


if __name__ == "__main__":
    main()
