# Shadowmail Flask App

## Testing

### Environment variables

    export APP_SETTINGS=Testing
    export DB_PASSWORD="change_me"
    export SECRET_KEY="change_me"
    export FLASK_APP=$(pwd)/main.py

### Run tests

    flask test

## Development

### Environment variables

    export APP_SETTINGS=Development
    export DB_PASSWORD="change_me"
    export SECRET_KEY="change_me"
    export FLASK_APP=$(pwd)/main.py
    export FLASK_DEBUG=1

### Install requirements

    pip install -r requirements.txt

### Create database

    flask initdb

### Static files

The development static files can be generated using

    gulp dev

or can be generated with watch enabled using

    gulp

### Run development server

    flask run

## Production

### Initialise database

    flask initdb

### Static files

The production static files can be generated using

    gulp prod
