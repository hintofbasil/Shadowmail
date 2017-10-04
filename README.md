# Shadowmail

## Usage

Generate random passwords for flask and postfix

    export FLASK_DB_PASSWORD=$(pwgen -Bs1 24)
    export POSTFIX_DB_PASSWORD=$(pwgen -Bs1 24)

Generate Flask secret key

    export FLASK_SECRET_KEY=$(pwgen -Bs1 48)

Set Postfix domain name

    export MAILNAME=shadowmail.co.uk

Set SSL certificate location

    export SSL_LOCATION=/path/to/certificates

Set Amazon S3 credentials

      export AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"
      export AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY"
      export AWS_REGION="AWS_REGION"

Launch docker containers

    docker-compose up -d
