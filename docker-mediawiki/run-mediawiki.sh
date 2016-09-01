echo "Stopping mediawiki container"
docker stop mediawiki 2> /dev/null

echo "Removing mediawiki container"
docker rm mediawiki 2> /dev/null

echo "Restarting mediawiki container"
docker run --name mediawiki \
	--link mysql:mysql \
	-p 8080:80 \
	-v /home/[user]/mediawiki/config/LocalSettings.php:/var/www/html/LocalSettings.php \
	-v /home/[user]/mediawiki/images:/var/www/html/images \
	-v /home/[user]/mediawiki/extensions:/var/www/html/extensions \
	-d synctree/mediawiki


