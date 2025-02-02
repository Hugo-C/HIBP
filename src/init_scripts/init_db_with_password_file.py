"""
Main app

Usage:
   init_db_with_password_file.py --download
   init_db_with_password_file.py <passwords-path>

Options:
    -h --help             Show this screen.
    --download            Download the rockyou password file from Github
    <passwords-path>     Absolute path to the password init file (1 password per line

"""

from docopt import docopt
from redis import Redis

from src.common import PasswordHasher, PasswordStorage


def init_db(file_path: str, db_client: Redis) -> int:
    """Return the number of password inserted in db"""
    hasher = PasswordHasher()
    storage = PasswordStorage(client=db_client)
    processed = 0
    with open(file_path) as file:
        for password in file:
            prefix = hasher.prefix(password)
            storage.add_password(prefix=prefix, password=password)
            processed += 1
    return processed


if __name__ == "__main__":
    args = docopt(__doc__)
    if args.get("--download"):
        print("not implemented yet")
        exit(0)
    elif password_path := args.get("<passwords-path>"):
        print(f"Initializing db with {password_path}")
        init_db(password_path)  # TODO get from env var
    # else docopt will show help
