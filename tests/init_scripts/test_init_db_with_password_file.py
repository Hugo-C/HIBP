import tempfile

import pytest

from src.common import PasswordHasher, PasswordStorage
from src.init_scripts.init_db_with_password_file import init_db


@pytest.mark.skip()  # TODO
def test_init_db(kvrocks):
    with tempfile.NamedTemporaryFile() as fp:
        # we could use https://hypothesis.readthedocs.io/en/latest/ for more diverse test set
        passwords = ["123", "456", "789"]
        for p in passwords:
            fp.write((p + "\n").encode())
        fp.flush()

        password_inserted = init_db(fp.name, db_client=kvrocks)

    assert password_inserted == len(passwords)
    hasher = PasswordHasher()
    storage = PasswordStorage(client=kvrocks)
    # Check a password NOT in the list
    assert storage.get_passwords(hasher.prefix("ABC")) == set()
    # Check a password IN the list
    password_expected = passwords[0]
    assert password_expected in storage.get_passwords(hasher.prefix(password_expected))
