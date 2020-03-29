#!/usr/bin/env python

from email.message import EmailMessage
from smtplib import SMTP
from ssl import SSLContext

def load_ssl_context():
    context = SSLContext()
    context.load_verify_locations(cafile='./postfix/test_certs/tls.crt')
    return context

def build_message():
    message = EmailMessage()
    message['Subject'] = 'Test'
    message['To'] = 'test@shadowmail.co.uk'
    message['From'] = 'Mr Tester <test@example.com>'
    message.set_content('Test email')
    return message

def send_mail():
    with SMTP('localhost') as client:
        client.ehlo()
        client.starttls(context=load_ssl_context())
        client.ehlo()
        client.send_message(
            build_message()
        )

def main():
    send_mail()

if __name__ == '__main__':
    main()
