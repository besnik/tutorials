# Virtual Environments in Python (Windows and Linux)

## Introduction
Virtual environments is a way to separate requirements of different applications and code for specific libraries and environment settings.

Different applications require different dependencies (e.g. libraries) in different versions. By installing everything into global environment of operating system there is very good chance of conflicts. Lets say application A requires logging module version 1.0 but application B requires logging module version 2.0. If package or library is named the same it is not possible to install both versions in one environment. Virtual Environment can help in this situation.

Virtual environment creates separate python environment by linking/copying necessary files into separate folder. This way we can safely install and configure libraries needed for specific application without affecting global or other virtual environment. 

The separation is achieved by creating separate directory for each virtual env where python files are copied. Note that virtual env directory where python executables are copied is separate thing from directory where sources are. 
For example you can store your virtual environments under `c:\dev\envs` and have projects stored under `c:\dev\projects\*`

It is important to activate virtual env before working with it. Activating will modify $PATH variable of operating system and makes sure `python` or `python3` executable from right directory is called. Once we are done working in virtual env it is important to deactivate it which will undo changes to $PATH variable.

## Creating virtual environment
Navigate into directory that should hold python executables for virtual environment.
For example `c:\dev\envs\sqlalchemy`

Now type:
`python -m venv`

## Activating virtual environment
Navitage into directory that holds executables for virtual environment and type:
`.\scripts\activate`

On linux you type `source ./bin/activate`

Depending if you run the command from cmd or powershell activate.bat or activate1.ps will be executed.
%PATH% variable will be adapted.

## Deactivate virtual environment
Navitage into directory that holds executables for virtual environment and type:
`.\scripts\deactivate`

On linux you type `deactivate` (command is created with running `activate` script).

## Managing libraries and versions
Note again that virtual environments with python executables are *independent* from your source code. Do not commit virtual environment files into source control system like Git or Svn.

To document what libraries and versions your code uses use `pip freeze` and `pip install`.

Use `pip freeze > requirements.txt` to save configured libraries and versions

Use `pip install -r requirements.txt` to install libraries needed to run code

## Helpers to simplify work with virtual environments
Switching between virtual environmetns and source code directories can require multiple commands. 
There are tools that can simplify those tasks.

### VirtualEnvWrapper
[Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) is tool with helper functions to easier switch and activate virtual environments.

**Installation**

Easiest way is to install using pip into global python:

Windows: `pip install virtualenvwrapper-win`

Linux: `pip install virtualenvwrapper`

Setup WORKON_HOME environment variable with directory where you have virtual environments (e.g. c:\dev\envs).

Add following files into your startup file (e.g. `.bashrc` or `.profile`) so the scripts are loaded into your shell:

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/dev
source /usr/local/bin/virtualenvwrapper.sh
```

See also [official installation](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) documentation.

**Create virtual environment**

Type (`myapp` is name of your virtual environment):

```
mkvirtualenv myapp
```

**Show list of available virtual environments**

```
workon
```

**Switch to virtual environment**
```
workon myapp
```

**Delete virtual environment**

Just delete folder where virtual environment was created. Path where virtual environments are created is specified by `WORKON_HOME` or look after default `.virtualenvs` folder in your home directory.

```
echo $WORKON_HOME
rm -rf ${WORKON_HOME}/myapp
```

**Useful commands**
 - `workon` - lists available environments
 - `workon <dir>` - activate specified env
 - `deactivate`
 - `mkvirtualenv <name>` - creates and activates virtual environment
 - `rmvirtualenv <name>` - removes the environment (uses folder_delete.bat)
 - `cdproject` - If a virtualenv environment is active and a projectdir has been defined, enters the project dir
 - `cd-` - returns you to the last directory before calling cdproject
 - `setprojectdir <full or relative path>` - sets project directory (where code is)

## Creating virtual environment using virtualenv

Installation (if not already present):

`sudo apt-get install virtualenv`

Check where is python executable you want to use for virtual env:
```
which python3
/usr/bin/python3
```

Create virtual env using python 3:

```
mkdir ~/venvs
virtualenv --python=/usr/bin/python3 ~/venvs/myapp
```

If there is problem with connecting to network check proxy settings (see linux-setup section) or firewall.

Activate: `source ~/venv/myapp/bin/activate`

Deactivate: `deactivate`

