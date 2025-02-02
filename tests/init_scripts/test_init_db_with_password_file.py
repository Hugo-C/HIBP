import pytest

from src.init_scripts.init_db_with_password_file import PasswordStorage

SOME_PREFIX = "01234A"


@pytest.fixture
def password_storage(kvrocks):
    yield PasswordStorage(client=kvrocks)


def test_get_password_should_return_empty_set_at_first(password_storage):
    assert password_storage.get_passwords(SOME_PREFIX) == set()

def test_get_password_should_return_added_password(password_storage):
    password = "some password"
    password_storage.add_password(prefix=SOME_PREFIX, password=password)

    assert password_storage.get_passwords(SOME_PREFIX) == {password}

def test_get_password_should_return_only_password_with_the_same_prefix(password_storage):
    password = "some password"
    password_storage.add_password(prefix=SOME_PREFIX, password=password)

    assert password_storage.get_passwords("00000") == set()

def test_get_password_should_return_all_password_added_for_a_given_prefix(password_storage):
    passwords = {
        "some password 1",
        "some password 2",
        "some password 3",
    }
    for password in passwords:
        password_storage.add_password(prefix=SOME_PREFIX, password=password)

    assert password_storage.get_passwords(SOME_PREFIX) == passwords


def test_get_password_should_discard_duplicates(password_storage):
    passwords = {
        "some password 1",
        "some password 2",
        "some password 3",
    }
    for password in passwords:
        # We add twice the same password
        password_storage.add_password(prefix=SOME_PREFIX, password=password)
        password_storage.add_password(prefix=SOME_PREFIX, password=password)

    assert password_storage.get_passwords(SOME_PREFIX) == passwords