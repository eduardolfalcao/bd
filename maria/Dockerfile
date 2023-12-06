FROM mariadb:10.5

COPY ./sql-script/ /docker-entrypoint-initdb.d/

EXPOSE 3306
CMD ["mysqld"]
