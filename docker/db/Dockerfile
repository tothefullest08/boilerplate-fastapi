FROM --platform=linux/amd64 mysql:5.7
MAINTAINER Harry <tothefullest08@gmail.com>

#ADD ./mysql-init-files /docker-entrypoint-initdb.d
ENV MYSQL_DATABASE=fastapi
ENV MYSQL_ROOT_PASSWORD=fastapi
EXPOSE 3306
CMD ["mysqld"]