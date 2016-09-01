# Running Mediawiki as Docker container

[Mediawiki](https://www.mediawiki.org) is popular wiki engine that besides other thins powers also Wikipedia. It is based on PHP and supports various SQL databases - preferably Mysql or Sqlite (for smaller deployments). During installation you can decide if you are going to use Sqlite or a standard sql service like Mysql.


# Getting docker image

For this demonstration we will use [synctree/mediawiki](https://hub.docker.com/r/synctree/mediawiki/) image from docker hub.

`docker pull synctree/mediawiki`


# Setup infrastructure on host

Create directory that will hold all persisted data related to media wiki.

For purpose of this tutorial we will create it in home directory of the user:

`mkdir ~/mediawiki`

Next we will create following sub-directories under `mediawiki` directory:

 - `config` - we will save here LocalSettings.php that installation script will generate. For sub-sequent start of container this file will be mounted to the mediawiki container.
 - `extensions` - custom extensions for mediawiki
 - `images` - holds image and uploaded files

To summarize - your directory structure should look like this:

```
~/mediawiki/
~/mediawiki/config/
~/mediawiki/extensions/
~/mediawiki/images/
```

We will configure mediawiki to run using separate mysql container so no need extra folder to store data. How to setup mysql container you can read in this tutorial reposistory as [separate article](/docker-mysql).

Note: if you decide to go for *sqlite* you don't need mysql instance or mysql container. During mediawiki installation in the browser just select sqlite and you will get full path where .db file of sqlite will be stored in container. On host create `~/mediawiki/db/` folder. It will contain sqlite data files. You will need to mount `db` directory from host to container during docker run so data are not lost.

# Installing mediawiki

Now we will start docker container for first time. 

```
docker run --name mediawiki \
        --link mysql:mysql \
        -p 8080:80 \
        -d synctree/mediawiki

```

System will detect that mediawiki is not yet configured and will offer installation wizard. During steps you will be asked for:

 - Mysql host or IP (use `docker inspect mysql` to find out IP address of the container with mysql if you run mysql as docker container)
 - In case of sqlite mark down full path where data will be stored!
 - User name for mysql
 - Password for mysql

Rest of the questions should be clear.

At the end the system will generate *LocalSettings.php*. Save it to the `/home/[user]/mediawiki/config/`. Mediawiki is asking you to copy the file into mediawiki direcotry. We will make use of mounting files using `-v` command to achieve that but before that we need to take care about few more things.

Note: in case something goes wrong or you need to restart installation process - just stop container and start it again. Everything will start from the scratch.


# Making content persistent on host 

Verify using `docker ps` that mediawiki container is running.

If yes we can continue. If no - use `docker logs mediawiki` to see what caused container to stop. You can use `docker logs mediawiki` command also during runtime of the container to see output and what's going on.

So at the moment mediawiki is configured in the db and `LocalSettings.php` file was generated and saved on the host (`~/mediawiki/config/`). 
Mediawiki image is coming with some content in `images` and `extensions` directories inside container we want to persist on host.
We are going to copy content of those directories from container to host. 

`docker cp mediawiki:/var/www/html/extensions ~/mediawiki`

`docker cp mediawiki:/var/www/html/images ~/mediawiki`

Note: in case of sqlite db you could use same approach and copy data from container to host.

Next we are going to run container and mount folders from host.


# Running mediawiki with persisted content

Now everything is ready to re-start our mediawiki container.

First lets stop and remove container so we can start from the scratch.

`docker stop mediawiki`

`docker rm mediawiki`

Now we will start container and mount folders from host with persisted content.

```
docker run --name mediawiki \
        --link mysql:mysql \
        -p 8080:80 \
        -v /home/[user]/mediawiki/config/LocalSettings.php:/var/www/html/LocalSettings.php \
        -v /home/[user]/mediawiki/images:/var/www/html/images \
        -v /home/[user]/mediawiki/extensions:/var/www/html/extensions \
        -d synctree/mediawiki
```

Note we are attaching single file into `/var/www/html/` directory on container.

In case of sqlite we would omit `--link` command and mount `/home/[user]/mediawiki/db` to the sqlite location on container.

It will take few seconds for system to start up everything. 

How you should have Mediawiki running as Docker container with persisted data, images (files), extensions and configuration.


# Next steps

Might be good idea to create some shell scripts to re-start mediawiki container.
Also script to attach shell to mediawiki container if needed to find/debug something.

It might be good idea to run container with automatic restart.

And explore docker compose to build everything in case your mediawiki container depends on other containers like mysql.

You can also configure extensions in `LocalSettings.php`. See mediawiki documentation how to do that for your version.
Also you might want to enable more file extensions for upload, added trusted media types or disable some checks for file upload, for example:

```
# allow uploading zip files and other extensions
$wgFileExtensions = array( 'png', 'gif', 'jpg', 'jpeg', 'doc',
    'xls', 'mpp', 'pdf', 'ppt', 'tiff', 'bmp', 'docx', 'xlsx',
    'pptx', 'ps', 'odt', 'ods', 'odp', 'odg', 'zip'
);

$wgTrustedMediaFormats[] = 'application/zip';  

# in case of problems with uploading files you could try to disable following checks:
#$wgVerifyMimeType = false;
#$wgStrictFileExtensions = false;
#$wgCheckFileExtensions = false;

```


Feedback and patches are welcomed!

Hope this helped.

