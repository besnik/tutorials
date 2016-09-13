# Linux setup

Following sections contains info how to configure Linux

## Environment variables

To configure system wide environment variables use `/etc/environment` file.

Alternatively you can use `export VARNAME=value` to setup environment variable in active session.

### Setup HTTP Proxy

If your system is behind proxy server you might need to configure few env variables so applications can 
find out which proxy server to use.

Add following lines into `/etc/environment` for system wide configuration:

```
HTTP_PROXY="http://proxy.company.com:1234"
HTTPS_PROXY="http://proxy.company.com:1234"
http_proxy="http://proxy.company.com:1234"
https_proxy="http://proxy.company.com:1234"
```

Unfortunately you have to add both uppper and lower case as different apps reads different keys.

## Creating user and group

Creating user

`sudo useradd <name>`

Creating user and group and specify shell + home directory:

`sudo useradd --system --gid <group+_name> --shell /bin/bash --home /home/<name> <name>`

Creating standard group:

`sudo groupadd <groupname>`

Creating system group (e.g. used for services):

`sudo groupadd --system <groupname>`

Swich to newly created user:

`sudo su - <name>`




