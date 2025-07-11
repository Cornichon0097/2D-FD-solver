# 2D-FD-solver

## Description

2D-FD solver for the time-dependent non-relativistic Schrödinger equation.

## Build

To build the solver, simply call the Makefile:

```sh
make
```

The Makefile will probably try to install some Python packages during the
process. Do not hesitate to use a virtual environment to avoid conflict between
Python packages.

```sh
python3 -m venv ./venv
source ./venv/bin/activate
```

## Configuration

### Settings

Change the [settings](./config/settings.json) file to match you authentification
information for the database access:

```json
    "mongodb":
    {
        "host": "<mongodb server>",
        "username": "<username>",
        "password": "<password>",
        "dbname": "2D-FD_solver",
        "collection": "<collection>"
    },
```

You can also change the logger settings and the output directory for VTK files.

```json
    "logger":
    {
        "level": "<debug | info | warning | error | critical>",
        "output": "<output>",
        "format": "%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S"
    },
```

### Parameters

Tweak the [parameters](./config/param.json) file if you want to:

```json
    "scheme": "<ftcs | btcs | ctcs>",
    "span": "<span>",

    "wave": "<wave function>",
    "args": [],

    "field": "<initial field>",
    "type": "<field type>"
```

Unfortunately, only the FTCS scheme is currently implemented. Using the other
ones would result in an empty computation.

The span defines the interval of time between each database insertion. Even if
MongoDB is fast, don't use a too short value. However, a too big value will
result in unusable VTK files.

The wave function can be defined as any of the function implemented in
[src/waves.py](./src/waves.py) (currently, only gaussian). The function will be
called during the initialization of the solver with the values in the args field
as parameters. The args field can contain both numeric value and named constant,
if it is defined in [src/const.py](./src/const.py):

```py
# Those specific constants are special values for the wave function available by
# there name in the configuration file (e.g., 1 / sqrt(2 * pi)).
CONSTANTS = {
    # "NAME": VALUE,
    "A": 1 / np.sqrt(2 * np.pi),
}
```

The solver will parse the constant name and replace it with its value. This way,
you can pass to the gaussian function values that are not writable in a JSON
file (e.g., root square).

The field property defines how the initial field should be generated. It can be
with a function, a constant matrix or even a file like an image. In first case,
you need to precise the type of the field generator as a "fun" type, and gives a
valid function name (defined in [src/fields.py](./src/fields.py)). To use a
file, give the path to it and change the type for a "path" type.

## Run

To rune the solver, simply call the `run` target in the Makefile:

```sh
make run
```

The solver will generate an initial VTK that you can check before continuing
the execution. If the generated VTK file does not meet your requirements, tweas
some parameters and rerun the solver.

If the solver is interrupted for some reason, during the next run, the solver
will retrieve documents from the previous one and restart where it stopped.
