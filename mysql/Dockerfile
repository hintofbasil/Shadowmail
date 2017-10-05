FROM mysql

ENV FLASK_DB_PASSWORD ""
ENV POSTFIX_DB_PASSWORD ""
ENV BACKUP_DB_PASSWORD ""

COPY ./docker-entrypoint-initdb.d /docker-entrypoint-initdb.d
