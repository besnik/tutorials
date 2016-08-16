# SQL Alchemy tutorial
This tutorial is collection of sample python code how to use SQL Alchemy Engine, MetaData, Expressions and ORM.
The tutorial is mainly based on presentation by Mike Bayer https://www.youtube.com/watch?v=woKYyhLCcnU

## Table of Contents
The code samples are divided into following groups (in that order):
 - Engine
 - MetaData
 - Expressions
 - ORM

The approach of learning is bottom-up - learn core things first (how to make raw SQL statements) 
and build on the top of it to learn how to use ORM and save domain models (objects) to the database of your choice.

Each group of code samples is numbered and named so you can quickly jump into section of your interest.

## Installation
If you want to run examples in virtual environment create and activate one first.

Install SQL Alchemy using `pip install sqlalchemy`

## IDE Configuration

### Visual Studio Code (Windows)
Configure `tasks.json` in `.vscode` directory to be able running the code using ctrl+shift+b.
If you don't use virtual environment and python is part of PATH global variable then command can be just "python".
To configure VSC with virtual environment you need to specify path to python.
Last change is to adapt "args" parameter to take current opened `${file}` as parameter when running python.

```javascript
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "0.1.0",
    "command": "c:\\path\\to\\python\\in\\virtualenv\\python.exe",
    "isShellCommand": true,
    "args": ["${file}"],
    "showOutput": "always"
}
```

To configure debugging with virtual environment adapt `launch.json` file in `.vscode` directory.
You will have to again specify path to python executable in virtual environment.

```javascript
{
    "version": "0.2.0",
    "configurations": [
         {
            "name": "Python (Alchemy virtual env)",
            "type": "python",
            "request": "launch",
            "stopOnEntry": true,
            "program": "${file}",
            "pythonPath": "c:\\path\\to\\python\\in\\virtualenv\\python.exe",
            "debugOptions": [
                "WaitOnAbnormalExit",
                "WaitOnNormalExit",
                "RedirectOutput"
            ]
        }
    ]
}
```

To support intellisense and autocomplete you need to define `python.autoComplete.extraPaths` in `settings.json` in `.vscode` directory.

```javascript
// Place your settings in this file to overwrite default and user settings.
{

    "python.autoComplete.extraPaths": [
    "c:\\path\\to\\python\\in\\virtualenv",
    "c:\\path\\to\\python\\in\\virtualenv\\Lib",
    "c:\\path\\to\\python\\in\\virtualenv\\Lib\\site-packages" ]
}
```

In case of problems, questions or suggestions feel free to send me message or patch. Thank you.