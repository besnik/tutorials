# Run MySql inside docker container

This tutorial and scripts will show you how to run official mysql image as docker container.

Configuration will satisfy following requirements:

 - data stored on mounted folder of the host
 - ability to customize mysql configuration
 - ability to dump whole database into .sql file to host

Next sections assumes you have docker engine installed on the host machine and know how to use basic docker commands.


# Getting mysql docker image

For this tutorial we will use [official Mysql docker image](https://hub.docker.com/_/mysql/).

To download image to your host simply type:
`docker pull mysql`

You can verify that your image is present on the host by typing:
`docker images`

Note: if you have existing/older container named mysql use `docker rmi mysql` command to remove image from the host.


# Setup host to store configuration, data and dumps

Next we prepare host system to store mysql data, configuration and place where to export sql dumps. We will make use mounting volume feature of docker.

For purpose of this tutorial we will organize all data into folder `mysql`. 

We will create the folder directly in your home directory:
`mkdir ~/mysql`

Note in production or test system it is better to have this directory under `/srv/` that serves as data for services in Linux.

Inside `mysql/` folder we will create new folders as following:

 - `conf.d/` - will be used to store mysql configuration files (.cnf) that overrides default configuration
 - `data/` - will store mysql data
 - `dumps/` - will store sql dumps we will make
 - `initdb.d/` - will store scripts (.sh, .sql, .sql.gz) to be executed when container is started for the first time

 
To summarize the folder structure should look like this:

```
~/mysql
~/mysql/conf.d/
~/mysql/data/
~/mysql/dumps/
~/mysql/initdb.d/
```

# Override default mysql configuration

By default mysql docker image loads configuration from container `/etc/mysql/my.cnf` which in turn loads 
configuration from `/etc/mysql/conf.d` and other places. To override default settings we will mount
folder `~/mysql/conf.d/` on host to the container. But first we need to create config file that will override
the values.

Navigate to `~/mysql/conf.d/` directory and create new file `mysql.cnf`.

Format of the file follows official Mysql configuration.

Example of custom `mysql.cnf`:

```
# This is custom config file attached from docker host

[mysql]
default_character_set = utf8

[mysqld]
character_set_server = utf8          # If you prefer utf8
collation_server = utf8_general_ci
```


# Executing scripts and sql on container startup

Putting any .sh or .sql or sql.gz files into folder `~/mysql/initdb.d/` will cause their execution on container startup
in alphabetical order.

Mysql image is internally looking to folder `/docker-entrypoint-initdb.d/` on the container. To override its content we will
mount `~/mysql/initdb.d/` from host to container.


# Starting mysql container

Now we will leverage all preparations we did on host and run mysql image as docker container.

```
docker run \
        --name mysql \
        -v /home/[user]/mysql/conf.d:/etc/mysql/conf.d \
        -v /home/[user]/mysql/initdb.d:/docker-entrypoint-initdb.d \
        -v /home/[user]/mysql/data:/var/lib/mysql \
        -e MYSQL_ROOT_PASSWORD=changeme \
        -d mysql

```

 - The above command will run mysql image as docker container with name `mysql`. 
 - Using `-v` parameter it will mount local volumes from host to container.
 - Using `-e` parameter we set environment variable inside container that image will use to setup mysql. See mysql image [documentation](https://hub.docker.com/_/mysql/) on docker hub for list of all available environment variables and their full description. In our case we will specify password that should be used when creating `root` user. This environment variable will remaing set during life time of the container.
 - Using `-d` parameter we will start image as daemon (service).
 - Last parameter specifies name of docker image to run.


Note: you can stop, remove and start mysql image as docker container. The data will be persisted thanks to `~/mysql/data/` mounted volume.

Note2: mysql now runs inside the container so it is visible *only* to host. If you want to expose it outsite of the host to separate servers run image with parameter `-p 3306:3306` that will map mysql port from container to host.

Note3: use `docker inspect mysql` to determine IP address of the container.


# How to attach shell to the mysql container or how to open mysql client on container?

You can connect to the running container using:
`docker exec -it mysql bash`

 - Using `-it` parameters you specify that you want to run command in interactive terminal mode.
 - mysql is name of container
 - bash is command that should be executed inside container

Once you are inside container you can connect to mysql service using mysql client and standard commands like:
`mysql --user=root --password=$MYSQL_ROOT_PASSWORD`

Note: if needed you could run docker exec mysql directly instead of bash.


# How to create full dump of mysql database?

It is possible to create full dump of mysql database running inside container. 
Then you can use generated .sql file to re-create db scructure and all data if needed (remember `~/mysql/initdb.d/` folder?).

To create full dump of mysql database running inside container and store it on the host in folder `~/mysql/dumps` type:
`docker exec mysql sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > /home/[user]/mysql/dumps/all-databases.sql`


# How to restore data from full dump?

Make use of `~/mysql/initdb.d/`. Copy .sql file(s) into the folder on the host and image will execute .sh, sql and .sql.gz when container will start.


# Next steps?

Try it out in your dev or test environment. 
You might want to build some shell scripts automate repetitive tasks like starting container, attaching shell or mysql client, or creating dump files.

In the repository I am attaching few very simple shell scripts for that. Make sure to set execute permissions on the .sh files using `chmod 774 <file>.sh`.

Feedback, ideas and patches are welcomed!

Hope this helped.
