# Deploy mongo as docker container with examples

This folder contains several ways how to deploy and use [mongo](https://docs.mongodb.com/manual/administration/install-community/) database as [docker container](https://hub.docker.com/_/mongo/) ([sources](https://github.com/docker-library/mongo)). Examples include basic shell script and docker-compose approach. Both have advantates and disadvantages. It depends on your requirements to pick up the right way to operate it. The tutorial is part of my [tutorials](https://github.com/besnik/tutorials) collection. Hope it helps.

The examples include:
- running mongo db in authenticated mode
- creating admin user, aplication user, backup user
- persistent storage
- dump and restore scripts (via docker container!)
- running mongo-express gui
- local vs prod docker compose files
- health check

## Prerequisities

- [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community) installed.
- [make](https://www.gnu.org/software/make/) tool for convenience (optional, very likely your linux already has it installed)
- Examples were tested on [Ubuntu Linux](https://ubuntu.com/download/desktop)

## Table of contents
1. Run mongo docker container via [shell script](1-run-script/).
2. Run mongo docker container via [docker-compose.yml](2-docker-compose/).

## Support

Feel free to ask question via Issues. PR are welcomed. Please leave a feedback.
