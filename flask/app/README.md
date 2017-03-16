# Shadowmail Flask App

## Test

### Initialise test environment variables

    export APP_SETTINGS=Development
    export DB_PASSWORD="change_me"
    export SECRET_KEY="change_me"
    export FLASK_APP=$(pwd)/main.py

### Run tests

    flask test
