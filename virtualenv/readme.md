# Virtual Environments in Python (Windows)

## Introduction
Virtual environments is a way to separate requirements of different applications and code for specific libraries and environment settings.

Different applications require different dependencies (e.g. libraries) in different versions. By installing everything into global environment of operating system there is very good chance of conflicts. Lets say application A requires logging module version 1.0 but application B requires logging module version 2.0. If package or library is named the same it is not possible to install both versions in one environment. Virtual Environment can help in this situation.

Virtual environment creates separate python environment by linking/copying necessary files into separate folder. This way we can safely install and configure libraries needed for specific application without affecting global or other virtual environment. 

The separation is achieved by creating separate directory for each virtual env where python files are copied. Note that virtual env directory where python executables are copied is separate thing from directory where sources are. 
For example you can store your virtual environments under `c:\dev\envs` and have projects stored under `c:\dev\projects\*`

It is important to activate virtual env before working with it. Activating will modify $PATH variable of operating system and makes sure `python` or `python3` executable from right directory is called. Once we are done working in virtual env it is important to deactivate it which will undo changes to $PATH variable.

## Creating virtual environment
Navigate into directory that should hold python executables for virtual environment.
For example c:\dev\envs\sqlalchemy

Now type:
`python -m venv`

## Activating virtual environment
Navitage into directory that holds executables for virtual environment and type:
`.\scripts\activate`

Depending if you run the command from cmd or powershell activate.bat or activate1.ps will be executed.
%PATH% variable will be adapted.

## Deactivate virtual environment
Navitage into directory that holds executables for virtual environment and type:
`.\scripts\deactivate`

## Managing libraries and versions
Note again that virtual environments with python executables are *independent* from your source code. Do not commit virtual environment files into source control system like Git or Svn.

To document what libraries and versions your code uses use `pip freeze` and `pip install`.

Use `pip freeze > requirements.txt` to save configured libraries and versions

Use `pip install -r requirements.txt` to install libraries needed to run code

## Helpers to simplify work with virtual environments
Switching between virtual environmetns and source code directories can require multiple commands. 
There are tools that can simplify those tasks.

### VirtualEnvWrapper
Virtualenvwrapper is tool with helper functions to easier switch and activate virtual environments.

**Installation**
`pip install virtualenvwrapper-win`

Setup WORKON_HOME environment variable with directory where you have virtual environments (e.g. c:\dev\envs)

**Useful commands**
 - `workon` - lists available environments
 - `workon <dir>` - activate specified env
 - `deactivate`
 - `mkvirtualenv <name>` - creates virtual environment
 - `rmvirtualenv <name>` - removes the environment (uses folder_delete.bat)
 - `cdproject` - If a virtualenv environment is active and a projectdir has been defined, enters the project dir
 - `cd-` - returns you to the last directory before calling cdproject
 - `setprojectdir <full or relative path>` - sets project directory (where code is)


