import pytest


def email_address_validator(email: str):
    if '@' not in email:
        return False
    return True


@pytest.mark.parametrize('email, expected_result', [
    ('daviddev@example.com', True),
    ('daviddevexample.com', False),
    ('magerko@example.com', True),
    ('magerkoexample.com', False),
    ('ilya@example.com', True),
    ('alina@example.com', True),
    ('kostya@example.com', True),
    ('katyaexample.com', False),
    ('kiraexample.com', False),
    ('chisaexample.com', False)
])
def test_email_address_validation(email: str, expected_result: bool):
    assert email_address_validator(email) == expected_result