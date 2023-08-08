FROM --platform=linux/amd64 mysql:5.7
MAINTAINER Harry <tothefullest08@gmail.com>

#ADD ./mysql-init-files /docker-entrypoint-initdb.d
ENV MYSQL_DATABASE=assignment
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=admin1234
ENV MYSQL_ROOT_PASSWORD=admin1234
ENV TZ=UTC

EXPOSE 3306
CMD ["mysqld"]