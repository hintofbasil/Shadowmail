#!/usr/bin/env python3

import base64
import html
import re
import traceback
import sys

from email.generator import Generator
from email.parser import Parser
from io import StringIO
from subprocess import Popen, PIPE

SENDMAIL_COMMAND = ['/usr/sbin/sendmail', '-G', '-i', '-f']

PLAINTEXT_FOOTER = """

----------

This email was originally sent from {from_email}

To delete this address visit: https://shadowmail.co.uk/request_delete?email={to_email}
"""

HTML_FOOTER = """<hr></hr>
<span>This email was originally sent from {from_email}</span>
<br></br><br></br>
<span>To delete this address visit: https://shadowmail.co.uk/request_delete?email={to_email}</span>
{closing_tag}"""

HTML_CLOSING_TAGS = ['</body>', '</BODY>', '</html', '</HTML>']

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

def add_plaintext_footer(part, email_to, email_from):
    content = part.get_payload()
    content += PLAINTEXT_FOOTER.format(
        to_email=email_to,
        from_email=email_from,
    )
    part.set_payload(content)

def add_html_footer(part, email_to, email_from):
    content = part.get_payload()
    for tag in HTML_CLOSING_TAGS:
        if tag in content:
            content = content.replace(
                tag,
                HTML_FOOTER.format(
                    to_email=html.escape(email_to),
                    from_email=html.escape(email_from),
                    closing_tag=tag,
                )
            )
            part.set_payload(content)
            return

def add_footer(email):
    (_, email_to) = get_name_and_email(email['To'])
    email_from = email['From']
    for part in email.walk():
        base64_encoded = part['Content-Transfer-Encoding'] == 'base64'
        encoding = part.get_charsets()[0]
        if base64_encoded:
            part.set_payload(base64.b64decode(part.get_payload()))
        if part.get_content_type() == 'text/plain':
            add_plaintext_footer(part, email_to, email_from)
        elif part.get_content_type() == 'text/html':
            add_html_footer(part, email_to, email_from)
        if base64_encoded:
            encoded_payload = base64.b64encode(part.get_payload().encode(encoding))
            encoded_payload_with_newlines = '\n'.join(
                [
                    encoded_payload[i:i+76].decode(encoding)
                    for i in range(0, len(encoded_payload), 76)
                ]
            )
            # We need this for the tests to pass as files in Unix systems should always
            # end with a new line
            encoded_payload_with_newlines = encoded_payload_with_newlines + '\n'
            part.set_payload(encoded_payload_with_newlines)
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
    return email

def main():
    try:
        email = get_email()
        email = add_footer(email)
        email = set_from_address(email)
        email = delete_blocking_headers(email)
        send_email(email)
    except Exception:
        sys.exit(75) # tempfail, we hope.

if __name__ == '__main__':
    main()
