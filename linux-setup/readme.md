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

Concepts: `HDDs` -> `Physical Volumes (PV)` -> `Volume Group (VG)` -> `Logical Volumes (LV)` -> `File System (FS)`

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

### How to enlarge / resize Physical Volume (Partition) and Logical Volume (LVM)

In general you need to follow these steps:

* Resize existing `physical volume (partition)` or add new physical volume
* Rezising existing PV should automatically create new free space in `Volume Group (VG)`. If addional physical volume (partition) was created, then it needs to be added to Volume Group (VG)
* Now that VG contains increased capacity you need to extend size of `Logical Partition (LV)`
* Last step is to resize `file system (FS)` on logical partition (LV) so you can use additional storage space

The below describes details on each step:

1. First take snapshot / backup image of your system in case something goes wrong!

 In case of VMware client or VirtualBox take snapshot.

2. Resize existing `Physical Volume (PV)` or create new Physical Volume.
 
 If you allow downtime of your server, easiest way would be to use `gparted` live image.
 Download live image `gparted` that allows you to modify partitions (PV) as you like. 
 Stop the server, boot from live iso image and resize existing partition or create new one.
 For this tutorial we will resize existing partition.
 
 Typically physical partition setup might look like this:
 HDD /dev/sda
 Partitions:
 - /dev/sda1
 - /dev/sda2 (Extended)
 - /dev/sda5 (Linux LVM)
 
 Look after partition you want to extend (in your case sda5) and its container (sda2 - extended partition)
 
 Before resizing: Devices must NOT be busy (mounted or locked). 
 You have to unmount sda5 before operation (right click in gparted on partition and click Disconnect)
  
 You need to first extend /dev/sda2 partition (that is container for sda5) and then extend /dev/sda5. 
 Write changes.
 After operation gparted should automatically mount and lock sda2 and sda5
 
 So now we have resized `Physical Volume (PV)`. 

 Unmount live cd and reboot.

3. Check `Volume Group (VG)` size
 
 Type `vgdisplay`
 
 This should show you `Alloc PC` and `Free PE` using `Cur PV` (current physical volumes)
 
 In Free PE you should see extra storage space you added to your physical volume (partition).
 
4. Resize `Logical Volume (LV)`

 Now we have new free storage space in Volume Group (VG). Lets increase storage in existing Logical Volume (LV).
 
 Type `lvdisplay` to list existing logical volumes. Pick up one you want to extend and look after its `LV Path`
 
 To resize the logical partition type (replace path template with value in `LV Path` for your logical partition):
 
 `lvextend -l +100%FREE /dev/volume-group-name/logical-volume-name`
 
5. Resize `File System (FS)`
 
 To make use of additional storage on logical volume we need to let file system know it can consume more space:
 
 Type following to resize file system (if you don't specify size it automatically allocates all free space)
 
 `resize2fs /dev/volume-group-name/logical-volume-name`
 
6. Done
 
 Enjoy. After testing you could remove backup snapshot to save some storage space.

## Logs

- `cat /var/log/syslog | less` - displays Linux syslog
- `grep sshd.\*Failed /var/log/auth.log | less` - displays failed SSH login attempts
- `grep sshd.*Did /var/log/auth.log | less` - displays failed connections
