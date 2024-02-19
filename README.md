# Installation

Open a terminal or powershell in the root directoy of the project then run the following code :

## Windows

```shell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## MacOS / Unix

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

# Dev environment setup

**Make sure tu use the correct python interpreter in your IDE.**

## PyCharm

On the bottom right, click on `Python 3.xx (worms)` (may also be `<No interpreter>`) then `Add New Interpreter > Add Local Interpreter...`
and check `Existing`.

Here the interpreter for the project should already be selected, or you will have to set it manually to this file : `.venv/bin/python`

(Also make sure that `Run Black` and `Optimize imports` are checked in `Settings > Tools > Actions on Save`)

## VSCode

The interpreter should already be selected, check the bottom right of the window, if you see `3.x.x ('.venv': .venv)`, it's all good !  
Otherwise click on it and select the `.venv/bin/python` interpreter.

# Run the project

## Windows

```shell
.\.venv\Scripts\activate
python worms_game.py
```
