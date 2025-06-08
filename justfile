set positional-arguments

default:
  just --list

@run *args:
  uv run python main.py {{ args }}

@status:
  just run status

@start *time:
  just run start {{ time }}

@stop:
  just run stop

@resume:
  just run resume

@cancel:
  just run cancel

@repeat:
  just run repeat

@help:
  just run help

shell:
   uv run ipython

fmt:
   ruff format *.py yapom/

lint:
   ruff check --fix *.py tests/*.py

check file:
   uv run pyright {{ file }}
