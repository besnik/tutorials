# Goal of the makefile is to simplify managing and operating application
# You need to install GNU Make on your operating system in order to call `make` command.
#	Windows: http://gnuwin32.sourceforge.net/packages/make.htm (make sure path to make.exe is added to PATH)
#	Ubuntu: make is already installed
# Call `make help` to see list of available commands

# Important: when editing use *tabs* (not spaces) otherwise Makefile won't work!
# Important: each line runs in *separated subprocess*. if you need to chain commands use: cmd1 && cmd2

# ---------
# Variables
# ---------
# Project root directory
PROJ_DIR=.
# Path to requirements
REQ=requirements.txt
# Python executable
PYTHON=python
# Pip executable
PIP=pip

# -------
# Targets
# -------

all: help

help:
	@echo Following commands helps to operate the project.
	@echo Make sure you are in project root directory and venv is active.
	@echo ----------------------------- OPS-------------------------------------
	@echo '   make build'
	@echo '        Installs pip dependecies.'
	@echo '   make doc'
	@echo '        Builds documentation.'
	@echo '   make serve'
	@echo '        Starts build-in web server to preview doc.'
	@echo ''

# ensures virtual env is activated
virtual_env_set:
ifndef VIRTUAL_ENV
	$(error Virtual environment $(VENV) is not active. Type `workon $(VENV)` to activate it)
endif

# builds project from scratch
# installs or upgrades dependencies using pip
build: virtual_env_set $(REQ)
	$(PIP) install --upgrade -r $(REQ)

# starts build-in web server that previews the doc
serve: virtual_env_set mkdocs.yml
	mkdocs serve

# builds documentation
doc: virtual_env_set mkdocs.yml
	mkdocs build --clean
