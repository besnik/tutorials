# Gunicorn

## Installation

`pip install gunicorn`

## Start server - simple

Navigate to your app (source) directory (e.g. it could be Django project root) and type :

`gunicorn myapp.wsgi:application --bind 0.0.0.0:8001`

The above examples starts gunicorn http server on port 8001 that will listen for any IP.
You could also specify concrete IP or hostname.

## Start server - robust

More complex apps will require more complex startup setup. This usually includes: 

* Activating virtual environment
* Installing requirements (using `pip` for python)
* Specifying path to configuration files for specific environment (dev vs test vs prod)
* Ensuring all necessary dependencies (e.g. files, directories) are setup
* Running gunicorn under specific user and group
* Configuring local sock for local interprocess communication (e.g. Nginx <-> Gunicorn)
* Configuring logging

Following shell script starts more complex Django application:

```
#!/bin/bash


NAME="MyApp"                                            # Name of the application
DJANGO_DIR=/var/www/myapp/src                           # Django project directory
DJANGO_REQ_DIR=$DJANGO_DIR"/requirements/test.txt"      # Path to requirements
DJANGO_WSGI_MODULE=myapp.wsgi                           # Django WSGI module name
DJANGO_SETTINGS_MODULE=myapp.settings.test              # settings for django project
GUNICORN_WORKERS=3                                      # number of working processes will be spawned (2 x cores + 1)
SOCKFILE=/var/www/myapp/sock/gunicorn.sock              # we will communicate using this unix socket with nginx
USER=myappuser                                          # the user to run as
GROUP=webapps                                           # the group to run as

echo "Staring $NAME as `whoami`"


cd $DJANGO_DIR


# Activate virtual environment
source ../venvs/myapp/bin/activate
which pip


# Install dependencies
pip install -r $DJANGO_REQ_DIR


# Setup environment variables
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGO_DIR:$PYTHONPATH

# Create the directory for socket file if it doesn't exist
SOCKDIR=$(dirname $SOCKFILE)
test -d $SOCKDIR || mkdir -p $SOCKDIR

# Start gunicorn
# Remove bind to IP/hostname+port once connected via socker with nginx
exec gunicorn $DJANGO_WSGI_MODULE:application \
  --name $NAME \
  --bind 0.0.0.0:8001 \
  --bind=unix:$SOCKFILE \
  --workers $GUNICORN_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=info \
  --error-logfile=- \
  --log-file=-
```

## Set nicer process titles

OPTIONAL: You might want to setup setproctitle to set pretty names of processes

`sudo apt install python-dev`
`(myapp)myappuser@server:~$ pip install setproctitle`

Then you can inspect running processes: `ps aux`

