#!/usr/bin/env bash

echo "=============START====================="
## php
echo '[php]yum install php php-fpm php-gd php-mcrypt php-pear php-mysql php-mysqlite'
yum install php php-fpm php-gd php-mcrypt php-pear php-mysql php-mysqlite
chkconfig php-fpm on

echo '[php]change php.ini date.timezone'
sed -i 's/^;date\.timezone\ =/date\.timezone\ =\ "Asia\/Shanghai"/' /etc/php.ini

sed -i 's/^user\ =\ apache/user\ =\ nginx/' /etc/php-fpm.d/www.conf
sed -i 's/^group\ =\ apache/group\ =\ nginx/' /etc/php-fpm.d/www.conf

## mysql
echo '[msyql]install mysql mysql-server'
yum install mysql mysql-server
chkconfig mysqld on

echo '[msyql]start mysqld'
service mysqld start
echo '[msyql]SET password of root:------------------>'
# BOC2015  shift 231
read SQLPWD
mysqladmin -u root password $SQLPWD

## nginx
echo '[nginx]install nginx'

echo '[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=0
enabled=1' >> /etc/yum.repos.d/CentOS-Base.repo

#yum makecache
yum install nginx
chkconfig nginxd on

# make home
echo 'mkdir /home/wwwroot/'
mkdir -p /home/wwwroot/logs
mkdir /home/wwwroot/default_site
touch  /home/wwwroot/default_site/index.php
echo '<?php phpinfo();' > /home/wwwroot/default_site/index.php

mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak

echo "[nginx] SET DOMAIN(ignore www,like baidu.com):--------------->"

read DOMAIN
confile="/etc/nginx/conf.d/${DOMAIN}.conf"
touch $confile

echo '
server {
  listen 80;
  charset utf-8;
' > $confile

echo "
  server_name  _ ${DOMAIN} www.${DOMAIN};
  root        /home/wwwroot/${DOMAIN}/;
  access_log  /home/wwwroot/logs/${DOMAIN}_access.log  main;
  error_log   /home/wwwroot/logs/${DOMAIN}_error.log;
" >> $confile

echo '
  location /{
    index  index.php index.html index.htm;
    if (!-e $request_filename){
      rewrite ^/(.*)$ /index.php/$1 last;
    }
    # Must www
    # if ($http_host !~ "^www\.domain\.com$") {
	  #   rewrite ^(.*) http://www.domain.com$1 permanent;
    # }
  }

  location ~ ^.+\.php{
    fastcgi_buffer_size 128k;
    fastcgi_buffers 32 32k;
    fastcgi_pass  127.0.0.1:9000;
    fastcgi_index index.php;
    fastcgi_split_path_info ^((?U).+\.php)(/?.+)$;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_param PATH_INFO $fastcgi_path_info;
    fastcgi_param PATH_TRANSLATED $document_root$fastcgi_path_info;
    include       fastcgi_params;
  }

  #error_page  404              /404.html;
  error_page   500 502 503 504  /50x.html;
  location = /50x.html {
    root   /usr/share/nginx/html;
  }

  # deny ci
	location ^~ /views|controllers|config {
		deny all;
	}

	# deny .ht
	location ~ /\.ht {
		deny  all;
	}

  # deny .git
  location ~ /\.git {
    deny all;
  }

  # location ~* ^.+\.(ico|gif|jpg|jpeg|png|html|htm|css|js|txt|xml|swf|wav)$ {
  #   # root   /home/http/object/static;
  #   access_log   off;
  #   expires      30d;
  # }
}
' >> $confile

echo '[php]start php-fpm'
service php-fpm start
echo '[nginx]start nginx'
service nginx start
echo '======================END=========================='
echo '[end]open the IP site,read phpinfo '
echo 'web: /home/wwwroot/'
echo 'nginx: /etc/nginx/conf.d/'
echo 'php: /etc/php.init /etc/php-fpm.d/www.conf'
echo 'mysql: /etc/my.ini'
