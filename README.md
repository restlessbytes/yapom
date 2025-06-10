<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/restlessbytes/yapom">
    <img src="yapom/resources/icons/Emojione_1F345_240px.svg.png" alt="yapom" width="80" height="80">
  </a>
  <h3 align="center">Yet Another POModoro app</h3>
</div>

## About this project

`yapom` is a simple command-line tool for managing [Pomodoro](https://en.wikipedia.org/wiki/Pomodoro_Technique) sessions, written in Python.

I wrote `yapom` because I wanted a Pomodoro timer that ...

* doesn't require a GUI but can instead be controlled from the comfort of the command-line
* runs "in the background", meaning you don't need to have an app open all the time
* has very few (*if any*) dependencies

## Getting started

### Prerequisites

- Python 3.10 or higher
- [Tk / Tcl](https://tkdocs.com/tutorial/install.html)
- [libnotify-bin](https://gitlab.gnome.org/GNOME/libnotify)

**NOTE 1** `libnotify-bin` installs the `notify-send` utility, which serves as a backup in case Tcl/Tk notifications fail.

**NOTE 2**

`yapom` was initially developed under an [Ubuntu-based Linux distribution](https://system76.com/pop/) using `notify-send` for user notifications as a "quick-and-dirty" solution since "notifications" weren't a primary focus at the time.

Later, when I switched to Tcl/Tk for notifications, `notify-send` remained as a fallback utility.

Removal of this dependency is planned for a future release.

### Installation

> **Disclaimer** This app was written for **Linux**. I do not know if it runs on macOS (*probably*) or Windows (*likely not*).

The recommended way for setting up `yapom` is to clone this Git repository and then run `install.py`:

``` shell
$ cd ~
$ git clone git@github.com:restlessbytes/yapom.git
$ cd yapom/
$ chmod +x main.py install.py
$ ./install.py
```

Cloning directly into `$HOME` is not strictly required, but strongly recommended.

## Usage

### Starting a Pomodoro session

The command

```shell
$ yapom start
```

starts a new Pomodoro session with a default duration of 25 minutes.

The duration of a Pomodoro session can be specified in one of two ways:

1. Specify duration in *number of seconds*:

```shell
$ yapom start 300
```

This would start a 5-minute Pomodoro session (*300 seconds equals 5 minutes*).

2. Specify duration by hours (`h`), minutes (`m`) and/or seconds (`s`):

```shell
$ yapom start 1h30m30s
```

In this example, the session length would be *1 hour, 30 minutes and 30 seconds*.

Note that time specifiers with a value of zero (*e.g.,* `0h`) can be omitted. For example, the following commands are equivalent:

```shell
$ yapom start
$ yapom start 25m
```

### Ending a Pomodoro session

A Pomodoro session ends automatically when the time is up. A notification (*either as a message box or desktop notification*) informs the user that a session has ended.

The user can end a session before the timer runs out using the `cancel` command:

```shell
$ yapom cancel
```

This would end the current session immediately.

### Pausing, resuming or restarting sessions

The `pause` or `stop` commands *pause* a Pomodoro session that is in progress. A paused session can be resumed using the `resume` command.

It's only possible to use `pause` (or `stop`) and `resume` if a session is *active* (*or "in progress"*):

```shell
$ yapom pause
$ yapom resume
```

The `pause` and `stop` commands are equivalent.

The `restart` or `reset` commands restart a running session, resetting the start time to the current time.

### Repeating sessions

The `repeat` command starts a new session with the same *duration* as the previous one:

```shell
$ yapom repeat
```

## Acknowledgments

- [open-pomodoro CLI](https://github.com/open-pomodoro/openpomodoro-cli) which sparked the idea of a *CLI-based* Pomodoro app.

- Credit for the *Pomodoro Emoji* image used in the Tcl notification message(s) goes to [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Emojione_1F345.svg) (_creative commons_)
