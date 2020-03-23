# Run mongo docker container via shell script

This example shows basic approach how to run mongo db as docker container using shell script. The example can be extended to add more complexity, limit resources, cpu, memory, etc as needed.

Note that this approach is similar to one with docker compose. In some cases when running standalone container it might be even more powerful as some parameters that are available in `docker run` command are not available in `docker-compose` way (unless you are in docker swarm).

## 1. Prepare directory structure on host OS

Mongo is a database and we need a persistent place where to store data. For this example we will prepare following directory structure:

```
/srv/mongo-4.2.3/backup/
/srv/mongo-4.2.3/db/
```
`db` folder will store data in persistent way on host OS.
`backup` folder will be used for db dumps and restores.

Next we need to setup apropriate permissions on both folders. Inside container the mongo process is running under identity of user with ID `999`. We need to ensure the user id (although it does not exist on host OS) has appropriate permissions. Grant read permission to yourgroup so you can access raw data for debugging if needed. No access for other users!

```
drw-r----- 3    999 yourgroup 4096 Mar 19 22:09 backup/
drwxr----- 4    999 yourgroup 4096 Mar 19 22:09 db/
```

Use `sudo chown 999:user backup db` to change owners of the folders.

Use `sudo chmod 740 db` and `sudo chmod 640 backup` to set apropriate read/write/execute permissions.

Note: mongo docker container needs `execute` permissions on `db` folder, otherwise it fails to start.

Great! Now we are ready to prepare shell script, get the docker image and run container.

## 2. Prepare shell script

You can inspect the [shell script](run_mongo.sh) in this repository for full source code. The example is kept simple for understanding what is going on. More complex example is in [2-docker-compose](../2-docker-compose/) example.

```
echo "stopping and removing container"
docker stop mongo 2> /dev/null
docker rm mongo 2> /dev/null

echo "starting container"
docker run -d --name mongo -p 127.0.0.1:27017:27017 \
    --memory 100m \
    -v /srv/mongo-4.2.3/db:/data/db \
    mongo:4.2.3 --auth
```

The script has two parts:
1. it stops and removes any existing docker container named `mongo`
2. it starts new docker container called `mongo` using mongo image

There are few things to note:
- `-d` runs container in backgroup (detached mode).
- `-p` maps IP and port on `host OS` into container. Note that we specify `127.0.0.1` so the db is exposed on host OS only to itself (and not to intranet/internet). This is security measure you should always consider.
- `--memory` limits available memory up to 100MB to the process (using kernel syscall). Did I already tell you that the container is just sophisticaly isolated process on host os? Adjust memory limit to your needs.
- `-v` maps directory from host OS to container. Any files written in the specified directory inside container will be actually written into the folder on host OS. This is one way to achieve persistent storage. It is very static way, suitable for standalone deployments like in this example.
- `mongo:4.2.3` specifies docker image name and tag. Always use tag with all versions to avoid different image problems in multiple environments. Avoid latest or stable generic tags.
- `--auth` tells mongo process to run with enabled authentication. You always want to run with authentication enabled except once case - when you create admin user. For that you temporarily remove the parameter, create admin user and enable it again. Don't forget to restart container.

## 3. Start mongo as docker container

Run the script or type `make rundb`.

```
./run_mongo.sh
```

## 4. Install mongo client

In order to access mongo db you need a client. If you already have your prefered way how to access mongo then you can skip this section.

[Mongo CLI](https://docs.mongodb.com/manual/mongo/) is low-level command line tool that enables you with access to the database. I recommend to install it on your local development environment. We will use it to create `admin` user.

The tool will be installed directly on `host OS` for your convenience so you can easily assess mongo like it was running directly on host system (and not inside container).

Follow official instructions at
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition

You are ONLY interested in packages (no need to install db itself since we are going to run it as docker container):
```
mongodb-org-shell
mongodb-org-tools
```

Since the shell script for starting mongo docker container is using default port number, we can directly run `mongo` command from the command line or type `make mongo`:
```
mongo
```

The command will connect us to mongo database and output will be:
```
MongoDB shell version v4.2.3
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("c2b82130-b9c8-4182-9b47-553b062d561b") }
MongoDB server version: 4.2.3
>
```

## 5. Create admin user

First we need to disable authentication otherwise nobody could do anything. Remove `--auth` parameter from shell script and run it.

Next start `mongo` client: 
```
mongo
```
Verify the output and make sure there are no errors.

Once you are connected to mongo db using mongo cli, select `admin` database. Our users will be created in this database. 

```
> use admin;
```

Once the database is set, we can create our first admin user:

```
db.createUser(
    {
        user: "admin",
        pwd: passwordPrompt(),
        customData: { 'description': 'the ultimate user and data administrator' },
        roles: [{ role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase", "root"]
    }
);
```

Verify output that user was sucessfully created.

Notes on user creation:
- `passwordPrompt()` will ask you to enter password
- `userAdminAnyDatabase` role has permissions to manage databases
- `readWriteAnyDatabase` role has permissions to access and modify data
- `root` role has all permissions and especially those that allows user to create another users.

Once the user is created, type `exit`, **enable authentication** in shell script by adding back the `--auth` parameter and restart container by running the script or type `make rundb`.
```
./run_mongo.sh
```

Do NOT forget to enable authentication!

## 6. What's next?

With admin user created and authentication enabled you can play with mongo! Create users, databases, json documents, etc.

I recommend you continue reading [2-docker-compose](../2-docker-compose/) example for more advanced scenarios including mongo container healthcheck, dump and restore scripts, aplication and backup users, mongo-express GUI (running of course as docker container) and much more.

If you liked the tutorial, please leave a feedback or send me a message so I can improve it even more. Thank you.
