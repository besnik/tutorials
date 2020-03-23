# Run mongo docker container via docker-compose

This example shows more advanced technique to run mongo db using `docker-compose.yml` file. 

## 1. Prerequisities

If you have made [1-run-script example](../1-run-script), you can skip this section. Just ensure you stop and remove any mongo container.

Using [1-run-script example](../1-run-script) setup following things:
- directory structure
- install mongo CLI

## 2. Defining docker-compose.yml

By definition [docker-compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications. You define your services (containers) in one or multiple YAML files and start them with one command. This is more standardized way towards operating multi-container apps as comparison to custom shell script(s).

[docker-compose.yml](docker-compose.yml) contains definition of running mongo db using `docker-compose`.

The important parts of the .yml file:

The below defines mongo service and name of the container:
```
services:
  mongo:
    container_name: mongo
```
Next we define command parameters, persistent volumes from host os that will be mapped into container, image name and tag from which we start container.
```
    command: --auth
    ports:
      - "127.0.0.1:27017:27017"
    volumes:
      - "/srv/mongo-4.2.3/db:/data/db"
    image: mongo:4.2.3
```
Specifing `127.0.0.1` ensures that the services will be accessible only from localhost. This is important security setting especially with docker that modifies linux IPTables configuration (and effectively bypasses firewall like [ufw](../uncomplicated-firewall-ufw)), which is responsible for allowing and denying inbound and outbound traffic.

The below specifies in which named network the container will run and what will be its name to other components in the network. In our case we will use network named `backend` and define `mongo` as network identifier for other components:
```
    networks:
      backend:
        aliases:
          - mongo
```
If you wonder where `backened` network is defined, look at the bottom of the .yml file:
```
networks:
  backend:
    name: backend

```
It is good practice to define backend and db components in one `backend network`, and webserver, frontend components in other `frontend network`. In case a hacker gets access to frontend network, it won't see the db as it is in other network. Typical example would be nginx and gunicorn containers in frontend network and gunicorn and db containers in backend network.

Next we specify restart policy:
```
    restart: always
```

The below is only taking into effect in docker swarm cluster:
```
    deploy:
      replicas: 1
      resources:
        limits:
          memory: 500M # adjust to your needs
      restart_policy:
        condition: any
        max_attempts: 3
```
Note: at the moment of writing this tutorial I did not find a way how to limit resources like cpu and memory using docker-file in single host scenario. This shows limitation of docker-compose approach in comparison to `docker run` via shell script or more robust approach like Kubernetes.

Next you always want to have the logging under control so you don't end up with tons of logs or out of storage:
```
    logging:
      driver: "json-file"
      options:
        max-size: "10M"
        max-file: "10"
```

Next we define limits on number of processes:
```
    ulimits:
      nproc: 5000
      nofile:
        soft: 10000
        hard: 40000
```
Override if you are not satisfied with default values.

It is very important to setup healthcheck to monitor status of your containers:
```
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongo localhost:27017/test --quiet
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 5s
```
This assumes mongo CLI is installed.

## 3. Running mongo db using docker-compose

You can start the db using `make updb` or via:
```
docker-compose -f docker-compose.yml up --detach 
```
The command specifies which .yml file to use as definition, `up` specifies to start the service and `--detach` indicates the service should run in backgroupd.

## 4. Stopping mongo db using docker-compose

Use `make down` or following command to shut down containers started using `docker-compose`:
```
docker-compose down --volumes
```
Note: you could also run `docker stop mongo` and `docker rm mongo`, `docker network rm backend` and `docker volume prune` to remove all parts manually.

## 5. Test vs Production docker-compose .yml files

`docker-compose` supports override of .yml file by another .yml file by chaining `-f` parameter. You can make advantage of this feature or create clean and reusable configuration between different environments.

For example you could organize your test and production service definition using two .yml files. By default all settings are production stored in `docker-compose.yml`. Next you override test specific setting in `docker-compose.test.yml` file. Now to start the service in test configuration run:
```
docker-compose -f docker-compose.yml -f docker-compose.test.yml up --detach 
```
If you want to start the service in production configuration run:
```
docker-compose -f docker-compose.yml up --detach 
```

## 6. Mongo-Express in local environment

[Mongo-Express](https://github.com/mongo-express/mongo-express) is simple web GUI for Mongo DB. You should run it only in your local dev environment. In this example we are going to start it as a docker container and only in local development environment.

For this we create new [docker-compose.local.yml](docker-compose.local.yml) file.

First part of the local compose file overrides `command` setting of `mongo` service definition:
```
services:
  mongo:
    command: --auth --wiredTigerCacheSizeGB 0.25
```

Second part definies Mongo-Express service:
```
  mongo-express:
    image: mongo-express:0.54.0
    container_name: mongo-express
    restart: always
    ports:
      - 127.0.0.1:8081:8081
    environment:
      ME_CONFIG_BASICAUTH_USERNAME: ${MONGO_EXPRESS_USER}
      ME_CONFIG_BASICAUTH_PASSWORD: ${MONGO_EXPRESS_PASS}
      ME_CONFIG_MONGODB_ADMINUSERNAME: ${MONGO_ADMIN_USER}
      ME_CONFIG_MONGODB_ADMINPASSWORD: ${MONGO_ADMIN_PASS}
      ME_CONFIG_MONGODB_PORT: 27017
      ME_CONFIG_MONGODB_SERVER: mongo
      ME_CONFIG_REQUEST_SIZE: "100kb"
    networks:
      backend:
        aliases:
          - mongo-express
```

You need to define few [environment variables](https://github.com/mongo-express/mongo-express#usage-docker), at minimum credentials to access mongo db and credentials to access Mongo-Express web GUI.

Also note `networks` configuration: here we tell docker to run container in `backend` network and give it `mongo-express` network name to other components in the network.

Since `mongo` and `mongo-express` containers are in same `backend` network, mongo-express can see mongo service and call its API. Note that value of `ME_CONFIG_MONGODB_SERVER` is the name of mongo container defined in [docker-compose.yml](docker-compose.yml).

To run both mongo and mongo-express containers type `make up` or run:
```
docker-compose -f docker-compose.yml -f docker-compose.local.yml up --detach 
```
Note that the second `-f` references local docker-compose file, that will override values specified in first `-f` file.

## Further steps

A natural next step forward from here is to look after [Kubernetes](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [OpenShift](https://docs.openshift.com/container-platform/4.3/applications/deployments/what-deployments-are.html) or similar platforms and their deployment configs. Complexity of the platforms, the architecture and deployment configuration is topic for another tutorial.
