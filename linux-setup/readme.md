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

## Permissions and ACL

Changing owner (user:group) of an item: `chown -R myappuser:ormaci /var/www/myapp`

Changing permissions recursively `chmod -R 660 /var/www/myapp/some_file`

Problem with default user:group permissions on file system is that they are not recursive for newly created/modified content.

To explicitely say who should have access to what make use of ACL (like in windows you can specify who can access parent folder and 
rules will automatically apply to the child items).

```
getfacl parent_dir
setfacl -Rdm g:mygroup:rwX parent_dir
setfacl -Rm g:mygroup:rwX parent_dir
getfacl parent_dir
```

- http://superuser.com/questions/151911/how-to-make-new-file-permission-inherit-from-the-parent-directory
- https://help.ubuntu.com/community/UbuntuLTSP/ACLSupport




