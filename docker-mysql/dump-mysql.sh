echo "Ensure mysql container is running"

docker exec mysql \
	sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > /home/[user]/mysql/dumps/all-databases.sql

echo "Dumps generated and stored in mysql/dumps directory"
