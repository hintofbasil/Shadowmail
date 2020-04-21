#!/usr/bin/env python3

import re
import traceback
import sys

from email.generator import Generator
from email.parser import Parser
from io import StringIO
from subprocess import Popen, PIPE

SENDMAIL_COMMAND = ['/usr/sbin/sendmail', '-G', '-i', '-f']

FOOTER = """

----------

This email was originally sent from {from_email}

To delete this address visit:\nhttps://shadowmail.co.uk/request_delete?email={to_email}
"""

EMAIL_ONLY_REGEX = re.compile(r'(.+@.+)')
NAME_AND_EMAIL_REGEX = re.compile(r'(["\']?)(.+)\1\s<(.+@.+)>')

def get_email():
    parser = Parser()
    return parser.parse(sys.stdin)

def send_email(email):
    command = SENDMAIL_COMMAND + [email['From']] + sys.argv[1:]
    subprocess = Popen(
        command,
        stdin=PIPE
    )
    in_mem_file = StringIO()
    generator = Generator(in_mem_file, mangle_from_=False)
    generator.flatten(email)
    subprocess.communicate(in_mem_file.getvalue().encode('utf-8'))
    return subprocess.wait()

def add_footer(email):
    content = email.get_payload()
    content += FOOTER.format(
        from_email=email['FROM'],
        to_email=email['To'],
    )
    email.set_payload(content)
    return email

def get_name_and_email(original_from):
    matcher = NAME_AND_EMAIL_REGEX.match(original_from)
    if matcher:
        name = matcher.group(2)
        email_address = matcher.group(3)
        return (name, email_address)
    matcher = EMAIL_ONLY_REGEX.match(original_from)
    if matcher:
        name = None
        email_address = matcher.group(1)
        return (name, email_address)
    return (None, 'unknown_sender@shadowmail.co.uk')


def escape_from(name, email_address):
    # If local email return early
    if email_address[-16:] == 'shadowmail.co.uk':
        return email_address
    safe_email = '{escaped_email}@shadowmail.co.uk'.format(
        escaped_email=email_address.replace('@', '#')
    )
    if name:
        return '"{name} (via ShadowMail)" <{email}>'.format(
            name=name,
            email=safe_email,
        )
    return '"{original_email} (via ShadowMail)" <{safe_email}>'.format(
        original_email=email_address,
        safe_email=safe_email,
    )

def delete_blocking_headers(email):
    del email['Sender']
    del email['Return-Path']
    del email['DKIM-Signature']
    return email

def set_from_address(email):
    (name, email_addess) = get_name_and_email(email['From'])
    new_from = escape_from(name, email_addess)
    with open('/tmp/new_email', 'a') as f:
        f.write(email['From'])
        f.write('\n')
        f.write(new_from)
        f.write('\n')
        f.write('\n')
    del email['From']
    email['From'] = new_from
    # email['From'] = 'noreply@shadowmail.co.uk'
    return email

def main():
    try:
        email = get_email()
        # email = add_footer(email)
        email = set_from_address(email)
        email = delete_blocking_headers(email)
        send_email(email)
    except Exception:
        with open('/tmp/err', 'w') as f:
            f.write(traceback.format_exc())
        sys.exit(75) # tempfail, we hope.

if __name__ == '__main__':
    main()
