![Continous Integration](https://github.com/hintofbasil/Shadowmail/workflows/Deploy/badge.svg)

# Shadowmail

A web website to create private email aliases.  These forward all emails on to your personal account but can be easily deleted should the address be leaked or sold.

This project is composed of three submodules.  The `flask` directory contains the backend, the `frontend` directory contains the frontend and the `postfix` directory contains the email client.

## Development

To bring up the development stack run the following.  The environment variables are optional but emails won't actually be sent without these.

```bash
export AWS_SMTP_USERNAME= # Your AWS SES username
export AWS_SMTP_PASSWORD= # Your AWS SES password
export MAILNAME="shadowmail.co.uk" # Your domain name to send/receive emails

docker-compose up
```

You can then access the site at http://localhost:8000

### Sending test emails

To send a test email to the development stack run

```bash
./send_test_email.py to@domain.co.uk (plain|html)
```

### Running tests

Instructions for testing can be found in the readme of each application

## Production

Instructions for deploying can be found in the readme of each application
