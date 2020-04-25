#!/usr/bin/env python

import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from smtplib import SMTP
from ssl import SSLContext

def load_ssl_context():
    context = SSLContext()
    context.load_verify_locations(cafile='./postfix/test_certs/tls.crt')
    return context

def build_message_plaintext_message(email):
    message = EmailMessage()
    message['Subject'] = 'Test'
    message['To'] = email
    message['From'] = 'Mr Tester <test@example.com>'
    message.set_content('Test email')
    return message

def build_message_html_message(email):
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Test'
    message['To'] = email
    message['From'] = 'Mr Tester <test@example.com>'

    html_part = MIMEText(
        '<html><body><h1>Test</h1></body></html>',
        'html',
    )
    plaintext_part = MIMEText(
        'Test email',
        'plain',
    )

    message.attach(html_part)
    message.attach(plaintext_part)

    return message

def send_mail(email, message_type):
    type_mapper = {
        'plain': build_message_plaintext_message,
        'html': build_message_html_message,
    }
    with SMTP('localhost') as client:
        client.ehlo()
        client.starttls(context=load_ssl_context())
        client.ehlo()
        client.send_message(
            type_mapper[message_type](email)
        )

def main():
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} email [plain|html]')
        exit(1)
    send_mail(*sys.argv[1:3])

if __name__ == '__main__':
    main()
