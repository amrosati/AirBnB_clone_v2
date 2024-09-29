#!/usr/bin/env bash
# Installs and configures Nginx to serve static content

SERVER_CONFIG=\
"server {
 	listen 80 default_server;
    listen [::]:80 default_server;

	server_name _;
 	index index.html index.htm;
	error_page 404 /404.html;
	add_header X-Served-By \$hostname;

	location / {
		root /var/www/html/;
        try_files \$uri \$uri/ =404;
	}

	location /hbnb_static/ {
		alias /data/web_static/current/;
		try_files \$uri \$uri/ =404;
	}

	if (\$request_filename ~ redirect_me) {
		rewrite ^ https://www.google.com permanent;
	}

	location = /404.html {
		root /var/www/error/;
		internal;
	}
}"
TEST_PAGE=\
"<!DOCTYPE html>
<html lang='en-US'>
	<head>
		<title>Home - HBnB</title>
	</head>
	<body>
		<h1>Welcome!</h1>
	</body>
</html>
"

if [[ "$(which nginx | grep -c nginx)" == '0' ]];
then
	apt-get update;
	apt-get install -y nginx;
fi

mkdir -p /var/www/html /var/www/error
chmod -R 755 /var/www
echo 'Hello World!' > /var/www/html/index.html
echo -e "Ceci n\x27est pas une page" > /var/www/error/404.html

mkdir -p /data/web_static/releases/test /data/web_static/shared
echo "$TEST_PAGE" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -hR ubuntu:ubuntu /data
bash -c "echo -e '$SERVER_CONFIG' > /etc/nginx/sites-available/default"
ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

if [ "$(pgrep -c nginx)" -le 0 ];
then
	service nginx start;
else
	service nginx restart;
fi
