# Shadowmail Frontend

This application hosts the frontend of the site.  This application handles all requests except those beginning with `/api/`.

## Testing

### Using docker compose

If you have launched the applcation in development mode using docker compose you can run the tests with

```bash
docker exec -e APP_SETTINGS=Testing shadowmail_frontend_1 make test
```

### Running locally

You can install dependencies and run the tests locally with

```bash
make install
make test
```

## Deployment

When developing the build should have a target of `development`.  This builds a Docker image which auto reloads changes and runs in a node environment.  When running in production the full Dockefile should be built.  This creates a Docker image which uses Nginx to host the static site.

### Commands

The following commands exist in development.

| command      | usage                            |
|--------------|----------------------------------|
| flask test   | Run the test suite               |
| flask initdb | Create the database tables       |
| serve        | Run the development server       |
| build        | Build the production application |
| test         | Run the unit and lint tests      |
| test:unit    | Run only the unit tests          |
| lint:fix     | Auto fix linting issues          |
| lint         | Run lint tests                   |


### Environment variables

This application has no configuration through environment variables.
