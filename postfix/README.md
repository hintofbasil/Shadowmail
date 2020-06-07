# Shadowmail Postfix

This application hosts an SMTP Postfix server to receive incoming emails.  It appends the email footer and forwards the email on to AWS SES to send out.  SES is used to keep a healthy reputation.

## Testing

### Using docker compose

If you have launched the applcation in development mode using docker compose you can run the tests with

```bash
docker exec -e APP_SETTINGS=Testing shadowmail_postfix_1 make test
```

### Running locally

You can install dependencies and run the tests locally with

```bash
make install
make test
```

## Deployment

The same Docker image is used in development and production.  If AWS SES credentials are provided emails will be forwarded.

### Environment variables

| variable          | type   | description                                                  |
|-------------------|--------|--------------------------------------------------------------|
| DB_USERNAME       | string | Username to access the database                              |
| DB_PASSWORD       | string | Password to access the database                              |
| DB_HOSTS          | string | Routable name to connect to the database (can be ip address) |
| AWS_SMTP_USERNAME | string | AWS SES username                                             |
| AWS_SMTP_PASSWORD | string | AWS SES password                                             |
| MAILNAME          | string | The mailname to use (e.g shadowmail.co.uk)                   |
