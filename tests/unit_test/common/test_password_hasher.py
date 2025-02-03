import pytest

from src.common import PasswordHasher


def test_prefix_is_5_char_long():
    hasher = PasswordHasher()
    assert len(hasher.prefix("some password")) == 5


def test_prefix_is_lowercase():
    hasher = PasswordHasher()
    assert hasher.prefix("some password").islower() is True


def test_prefix_is_hexadecimal():
    hasher = PasswordHasher()
    try:
        int(hasher.prefix("some password"), 16)
    except ValueError:
        pytest.fail("prefix is NOT hexadecimal")


def test_password_hasher():  # just to make sure hash does not change overtime
    hasher = PasswordHasher()
    assert hasher.prefix("some password") == "a4214"
