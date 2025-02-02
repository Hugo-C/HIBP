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
import os
import time

from docopt import docopt
from redis import Redis

from src.common import PasswordHasher, PasswordStorage

KVROCKS_HOST = os.environ.get("KVROCKS_HOST", "localhost")
KVROCKS_PORT = int(os.environ.get("KVROCKS_PORT", "6666"))



def init_db(file_path: str, db_client: Redis) -> int:
    """Return the number of password inserted in db"""
    print("")  # allow print below to clear this line return
    hasher = PasswordHasher()
    storage = PasswordStorage(client=db_client)
    processed = 0
    with open(file_path) as file:
        for line in file:
            password = line.strip()
            prefix = hasher.prefix(password)
            storage.add_password(prefix=prefix, password=password)
            processed += 1
            if processed % 100 == 0:
                print(f'\r{processed=}', end="")
    return processed


if __name__ == "__main__":
    import sentry_sdk
    sentry_sdk.init(
        dsn="XXX",
        traces_sample_rate=1.0,
    )

    args = docopt(__doc__)
    if args.get("--download"):
        print("not implemented yet")
        exit(0)
    elif password_path := args.get("<passwords-path>"):
        print(f"Initializing db with {password_path}")
        start = time.time()
        redis_client = Redis(host=KVROCKS_HOST, port=KVROCKS_PORT)
        sentry_sdk.profiler.start_profiler()
        init_db(password_path, db_client=redis_client)
        sentry_sdk.profiler.stop_profiler()
        duration = time.time() - start
        print(f"{duration=}")
    # else docopt will show help
