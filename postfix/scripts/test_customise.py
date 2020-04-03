from customise import get_name_and_email, escape_from

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
