# SQL Alchemy tutorial
This tutorial is collection of sample python code how to use SQL Alchemy Engine, MetaData, Expressions and ORM.
The tutorial is mainly based on presentation by Mike Bayer https://www.youtube.com/watch?v=woKYyhLCcnU

## Table of Contents
The code samples are divided into following groups (in that order):
 - Engine
 - MetaData
 - Expressions
 - ORM
 - Custom (advanced topics like composite foreign keys or composite primary keys)

The approach of learning is bottom-up - learn core things first (how to make raw SQL statements) 
and build on the top of it to learn how to use ORM and save domain models (objects) to the database of your choice.

Each group of code samples is numbered and named so you can quickly jump into section of your interest.

## Installation
If you want to run examples in virtual environment create and activate one first.

Install SQL Alchemy using `pip install sqlalchemy`

## IDE Configuration

### Visual Studio Code
Define path to python executable and libraries in `settings.json` in `.vscode` directory.
This could be path to your global python installation or to virtual env.
If you don't use virtual environment and path to python is part of `PATH` 
environment variable then `python.pythonPath` can be just "python" (or "python3"
on some Linux distribution if you intent to run Python 3).
In the example below we use virtual env:

```javascript
# On linux specify path in linux format
{
    "python.pythonPath":"c:\\path_to_venv\\Scripts\\python.exe",
    "python.autoComplete.extraPaths": [
    "c:\\path_to_venv",
    "c:\\path_to_venv\\Lib",
    "c:\\path_to_venv\\Lib\\site-packages"
    ]
}
```
Note: you can determine path to python by typing
`pip --version`. This prints path to currently active python environment
(work virtual env make sure the env is activated).

Next configure `tasks.json` in `.vscode` directory to be able running 
the code using `ctrl+shift+b`. Note change to `command` and `args` parameters.

```javascript
{
    "version": "0.1.0",
    "command": "${config.python.pythonPath}",
    "isShellCommand": true,
    "args": ["${file}"],
    "showOutput": "always"
}
```

To enable debugging configure `launch.json` file in `.vscode` directory.
Note `pythonPath` and `program` parameters.

```javascript
{
    "version": "0.2.0",
    "configurations": [
         {
            "name": "Python",
            "type": "python",
            "request": "launch",
            "stopOnEntry": true,
            "pythonPath": "${config.python.pythonPath}",
            "program": "${file}",
            "cwd": "${workspaceRoot}",
            "debugOptions": [
                "WaitOnAbnormalExit",
                "WaitOnNormalExit",
                "RedirectOutput"
            ]
        },
    ]
}
```



In case of problems, questions or suggestions feel free to send me message or patch. 
Thank you.