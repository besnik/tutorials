# This is very basic skeleton of script to run mongo database
# as docker container from mongo docker image.

# Authentication is enabled using --auth switch.
# Remove the switch to disable authentication, e.g. to 
# create admin user. Once the user is created, enable
# the switch and restart the container by running this script.

echo "stopping and removing container"
docker stop mongo 2> /dev/null
docker rm mongo 2> /dev/null

echo "starting container"
docker run -d --name mongo -p 127.0.0.1:27017:27017 \
    --memory 100m \
    -v /srv/mongo-4.2.3/db:/data/db \
    mongo:4.2.3 --auth
