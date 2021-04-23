FROM mariadb:10.5

COPY ./sql-scripts/ /docker-entrypoint-initdb.d/

EXPOSE 3306
CMD ["mysqld"]
