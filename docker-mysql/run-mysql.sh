echo "stopping mysql container"
docker stop mysql 2> /dev/null

echo "removing mysql container"
docker rm mysql 2> /dev/null

echo "re-starting mysql container"
docker run \
	--name mysql \
	-v /home/[user]/mysql/conf.d:/etc/mysql/conf.d \
	-v /home/[user]/mysql/initdb.d:/docker-entrypoint-initdb.d \
	-v /home/[user]/mysql/data:/var/lib/mysql \
	-e MYSQL_ROOT_PASSWORD=changeme \
	-d mysql

echo "mysql container should be running now. Port 3306 should be exposed on container"
