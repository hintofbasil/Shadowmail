# Shadowmail

## Usage

Generate random passwords for flask and postfix

    export FLASK_DB_PASSWORD=$(pwgen -Bs1 24)
    export POSTFIX_DB_PASSWORD=$(pwgen -Bs1 24)

Lanuch docker containers

    docker-compose up -d
