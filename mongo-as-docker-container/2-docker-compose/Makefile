# Goal of the makefile is to simplify managing and operating application
# You need to install GNU Make on your operating system in order to call `make` command.
#	Windows: http://gnuwin32.sourceforge.net/packages/make.htm (make sure path to make.exe is added to PATH)
#	Ubuntu: make is already installed
# Call `make help` to see list of available commands

# Important: when editing use *tabs* (not spaces) otherwise Makefile won't work!
# Important: each line runs in *separated subprocess*. if you need to chain commands use: cmd1 && cmd2


# -------
# Targets
# -------

all: help

help:
	@echo Following commands can help you to operate the project.
	@echo ''
	@echo ----------------------------- DOCKER-COMPOSE--------------------------------
	@echo '   make updb'
	@echo '        Starts mongo db as docker container using docker-compose.'
	@echo '   make up'
	@echo '        Starts apps as set of docker containers using docker-compose.'
	@echo '   make down'
	@echo '        Stops apps with all related docker containers using docker-compose.'
	@echo '   make logs'
	@echo '        Shows logs from all containers.'
	@echo '   make pull'
	@echo '        Pulls latest images required to run app.'
	@echo '   make validate'
	@echo '        Checks docker-compose configuration.'
	@echo '   make top'
	@echo '        Shows processes from all containers.'
	@echo ------------------------------ MONGO CLI -----------------------------------
	@echo '   make mongo'
	@echo '        Connects CLI to the mongo service running at localhost'
	@echo '   make mongo-admin'
	@echo '        Connects CLI to the mongo service running at localhost'
	@echo ''


############################
## MONGO CLI
############################

# runs mongo client and connects to the mongo at localhost.
mongo:
	mongo

# runs mongo client and connects to the mongo at localhost.
# this target expects the credentials stored as environment variables
mongo-admin:
	mongo -u ${MONGO_ADMIN_USER} -p ${MONGO_ADMIN_PASS} --authenticationDatabase admin

############################
## DOCKER COMPOSE
############################

# Pulls an image associated with a service defined in a docker-compose.yml, but does not start containers based on those images.
# https://docs.docker.com/compose/reference/pull/
pull: docker-compose.yml
	docker-compose pull 

# starts mongo db via docker-compose
# https://docs.docker.com/compose/reference/up/
updb: docker-compose.yml
	docker-compose -f docker-compose.yml up --detach 

# starts application using containers via docker-compose
# https://docs.docker.com/compose/reference/up/
up: docker-compose.yml
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up --detach 

# stops application via docker-compose
# https://docs.docker.com/compose/reference/down/
down: 
	docker-compose down --volumes

validate: docker-compose.yml
	docker-compose config

logs: docker-compose.yml
	docker-compose logs

top: docker-compose.yml
	docker-compose top
