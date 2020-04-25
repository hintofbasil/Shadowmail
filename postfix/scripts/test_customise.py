from customise import (
    get_name_and_email,
    escape_from,
    delete_blocking_headers,
    add_footer,
)

from email.message import EmailMessage
from email.parser import Parser

import pytest

@pytest.mark.parametrize(
    'original,expected_name,expected_email',
    [
        (
            'test@example.com',
            None,
            'test@example.com'
        ),
        (
            'Anna Test <test@example.com>',
            'Anna Test',
            'test@example.com'
        ),
        (
            '"Bob Test" <test@example.com>',
            'Bob Test',
            'test@example.com'
        ),
        (
            "'Cara Test' <test@example.com>",
            'Cara Test',
            'test@example.com'
        ),
        (
            '"no-reply@example.com" <no-reply@example.com>',
            'no-reply@example.com',
            'no-reply@example.com'
        ),
    ]
)
def test_get_name_and_email(original, expected_name, expected_email):
    (actual_name, actual_email) = get_name_and_email(original)
    assert actual_name == expected_name
    assert actual_email == expected_email


@pytest.mark.parametrize(
    'name,email,expected',
    [
        (
            None,
            'test@example.com',
            '"test@example.com (via ShadowMail)" <test#example.com@shadowmail.co.uk>'
        ),
        (
            'Anna Test',
            'test@example.com',
            '"Anna Test (via ShadowMail)" <test#example.com@shadowmail.co.uk>'
        ),
    ]
)
def test_escape_from(name, email, expected):
    new_from = escape_from(name, email)
    assert new_from == expected


def test_delete_blocking_headers():
    message = EmailMessage()
    message['Sender'] = ''
    message['Return-Path'] = ''
    message['DKIM-Signature'] = ''
    message = delete_blocking_headers(message)

    assert not hasattr(message, 'Sender')
    assert not hasattr(message, 'Return-Path')
    assert not hasattr(message, 'DKIM-Signature')

def load_test_email(name):
    with open(f'test_emails/{name}', 'r') as email_file:
        with open(f'test_emails/{name}_expected', 'r') as expected_file:
            parser = Parser()
            return (
                parser.parse(email_file),
                expected_file.read(),
            )

@pytest.mark.parametrize(
    'name',
    [
        'http_7bit',
        'http_7bit_no_body',
        'plaintext_7bit',
        'multipart_7bit',
        'http_base64',
        'plaintext_base64',
        'plaintext_to_named'
    ]
)
def test_add_footer(name):
    (email, expected) = load_test_email(name)
    email = add_footer(email)

    actual = email.as_string()

    assert actual == expected
