# yttg-server

## Prerequisites

- [Python](https://www.python.org/) 3.14 or newer

## Installation

First, clone the repo to the target machine

```shell
git clone https://github.com/BesserwisserErsterKlasse/yttg-server
```

Change into the project directory

```shell
cd yttg-server
```

Create a virtual environment

```shell
python3.14 -m venv .venv
```

And activate it

- On Linux / macOS

```shell
source .venv/bin/activate
```

- On Windows (PowerShell)

```shell
.venv\Scripts\Activate.ps1
```

Install the dependencies

```shell
pip install -e ".[optimize]"
```

**Note:** `[optimize]` is an optional dependency — you can omit it and run `pip install -e .`

Run the `main.py` file

```shell
python -O src/main.py
```

**Note:** `-O` is an optional flag that removes unnecessary `assert`s — you can omit it and run `python src/main.py`

## License

yttg-server is a free, open-source software distributed under the [AGPLv3 License](LICENSE.txt)
