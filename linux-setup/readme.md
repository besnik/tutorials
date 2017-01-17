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

## Logical Volume Management (LVM) on Linux

Concepts: `HDDs` -> `Physical Volumes (PV)` -> `Volume Group (VG)` -> `Logical Volumes (LV)`

Where:

- `HDDs`: physical hard drives.
- `Physical Volumes (PV)`: you can partition each HDD as needed.
- `Volume Group (VG)`: from many HDDs and their physical volumes (partitions) you create Volume Group(s) (VG). This is combined storage space from all partitions from all HDDs. It acts like one big drive (like cloud that you can easily scale).
- `Logical Volumes (LV)`: create Logical Volumes (like virtual disks) as needed (LV for operating system, LV for swap, LV for /home, LV for static data, LV for volatile data, etc)

LVM concept allows you to create partitions that would not be possible with HDDs.
For example, take two HDDs where each has capacity of 10GB. With LVM you could combine both into 20GB Volume Group and create two partitions (Logical Volume) of capacity 15GB and 5GB. As bonus you can dynamically increase Volume Group as you add more physical HDDs into system.

Useful commands to display info in console: 

- HDDs: `lsblk` (displays hdds, their partitions and logical volumes)
- Physical Volumes (PV): `fdisk -l` (displays list of partitions)
- Volume Group (VG): `vgdisplay --verbose` (displays info about volume group, which physical volumes (hdds and partitions) are used to create VG)
- Logical Volumes (LV): `lvdisplay --verbose` (displays info about logical volumes and to which VG they belong)

