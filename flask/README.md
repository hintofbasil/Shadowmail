# Shadowmail Flask App

This application hosts the backend for the site.  All of the routes begin with `/api/` so you will need to route requests begining with `/api/` here instead of the frontend.

## Testing

### Using docker compose

If you have launched the applcation in development mode using docker compose you can run the tests with

```bash
docker exec -e APP_SETTINGS=Testing shadowmail_backend_1 make test
```

### Running locally

You can install dependencies and run the tests locally with

```bash
make install
make test
```

## Deployment

The same docker image is used in development as production.  Settings which help with development can be disabled with environment variables.  Ensure you always change `APP_SETTINGS` to `Production` and `SECRET_KEY` to a randomly generated string with a sufficiently high entropy to be cryptographically secure.

### Commands

The following commands exist.  These require the setting of the environment variables below

| command      | usage                      |
|--------------|----------------------------|
| flask test   | Run the test suite         |
| flask initdb | Create the database tables |


### Environment variables

The following environment variables are used to configure this Docker image

| variable     | type    | default       | options                               |
|--------------|---------|---------------|---------------------------------------|
| PORT         | integer | 8000          |                                       |
| APP_SETTINGS | string  | "Development" | "Testing", "Deleopment", "Production" |
| DB_PASSWORD  | string  | "change_me"   |                                       |
| SECRET_KEY   | string  | "change_me"   |                                       |
| FLASK_DEBUG  | bool    | 1             | 0, 1                                  |
| RELOAD       | string  | ""            | "", "--reload"                        |
| APP_HOME     | string  | "/app"        |                                       |
