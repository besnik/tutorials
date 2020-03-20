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
	@echo ------------------------------ DB ------------------------------------
	@echo '   make rundb'
	@echo '        Runs mongo as docker container'
	@echo '   make mongo'
	@echo '        Connects CLI to the mongo service running at localhost'
	@echo '   make mongo-admin'
	@echo '        Connects CLI to the mongo service running at localhost'
	@echo '   make down'
	@echo '        Stops mongo docker container'
	@echo ''


############################
## DB
############################

# starts all databases required to operate app
# remove "--auth" parameter from run_mongo.sh script to disable authentication mode.
rundb: run_mongo.sh
	./run_mongo.sh

# runs mongo client and connects to the mongo at localhost.
mongo:
	mongo

# runs mongo client and connects to the mongo at localhost.
# this target expects the credentials stored as environment variables
mongo-admin:
	mongo -u ${MONGO_ADMIN_USER} -p ${MONGO_ADMIN_PASS} --authenticationDatabase admin

# stops mongo container
down:
	docker stop mongo
	docker rm mongo
