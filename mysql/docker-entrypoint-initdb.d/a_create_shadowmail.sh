#!/bin/sh
cat << EOF >> /docker-entrypoint-initdb.d/create_shadowmail.sql
CREATE USER 'flask'@'172.18.%.%' IDENTIFIED BY '$FLASK_DB_PASSWORD';
CREATE USER 'postfix'@'172.18.%.%' IDENTIFIED BY '$POSTFIX_DB_PASSWORD';

GRANT INSERT ON shadowmail.virtual_alias TO 'flask'@'172.18.%.%';
GRANT UPDATE ON shadowmail.virtual_alias TO 'flask'@'172.18.%.%';
GRANT SELECT ON shadowmail.virtual_alias TO 'postfix'@'172.18.%.%';

FLUSH PRIVILEGES;
EOF
