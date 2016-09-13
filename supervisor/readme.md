# Supervisor

## Installation

`sudo apt-get install supervisor`

Bin directory `/usr/bin/supervisor`, `/usr/bin/supervisorctl`


## Check status

See if supervisor is running (as root): `service --status-all`

See status of monitored processes by supervisor:
`supervisorctl status`

Find linux processes for "myapp"
`ps aux | grep myapp`


## Start / Stop

```
service supervisor start
service supervisor restart
```

Staring and stopping single app:

```
supervisorctl start myapp
supervisorctl stop myapp
supervisorctl restart myapp
```


## Configuration

Configuration of supervisor service itself stored in `/etc/supervisor/supervisord.conf`

Configurations of monitored processes are stored here: `/etc/supervisor/init.d/`

Supervisor init script: `/etc/default/supervisor`


### Reloading Configuration

```
supervisorctl reread
supervisorctl update 
```

Next we need to start app

`supervisorctl start myapp`


### Configure process to be monitored and started automatically

Create configuration for application: `/etc/supervisor/conf.d/myapp.conf`

Example of configuration file:

```
[program:myapp]
command = /var/www/myapp/start_app.sh                                   ; Command to start app
directory = /var/www/myapp                                              ; CD this directory before running command
autostart = true                                                        ; starts commad on system boot
autorestart = unexpected                                                ; auto restart command if it exists unexpectedly
stopasgroup = true                                                      ; send stop signal to whole process group (ensure child processes are killed to)
killasgroup = true                                                      ; sends SIGKILL to whole process group that will take care about children
startretries = 3                                                        ; number of retries before command is considered failed
user = myappuser                                                        ; User to run as
stdout_logfile = /var/www/myapp/logs/gunicorn_supervisor.out.log        ; Where to write log messages
stdout_logfile_maxbytes = 10MB
stdout_logfile_backups = 10
stderr_logfile = /var/www/myapp/logs/gunicorn_supervisor.err.log        ; wehre to write error messages
stderr_logfile_maxbytes = 10MB
stderr_logfile_backups = 10
redirect_stderr = false                                                 ; Save stderr in the same log
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8                         ; Set UTF-8 as default encoding

```
Once done you need to reload configuration and start app (see Reloading Configuration section).


### Configure logging

```
[supervisord]
logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
logfile_maxbytes=20MB
logfile_backups=10
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor  ; ('AUTO' child log dir, default $TEMP)
loglevel=info                    ; available values: critical, error, warn, info, debug, trace, or blather

```


### Allow users to run supervisor commands without sudo / root

```
groupadd supervisor
usermod -a -G supervisor `whoami`
```

Update `/etc/supervisor/supervisord.conf` (note changes to chmod 0770 and chown):

```
; supervisor config file

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
chmod=0770                      ; sockef file mode (default 0700) to owner and group
chown=root:supervisor           ; add also group supervisor for socket file

```


### Enable supervisor web UI

Update `/etc/supervisor/supervisord.conf` and add:

```
[inet_http_server]
port = 9001
username = admin
password = supersecretpwd
```

The supervisor web is protected by basic authentication with credentials defined as above.

# Further reading

- https://bixly.com/blog/supervisord-or-how-i-learned-to-stop-worrying-and-um-use-supervisord/
- http://supervisord.org/configuration.html
- http://supervisord.org/installing.html
- https://serversforhackers.com/monitoring-processes-with-supervisord
- http://www.onurguzel.com/supervisord-restarting-and-reloading/
- https://docs.docker.com/engine/admin/using_supervisord/

