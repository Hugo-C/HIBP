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

import tempfile
import time

import httpx
import rich
from docopt import docopt
from redis import Redis
from rich import print
from rich.progress import MofNCompleteColumn, Progress, SpinnerColumn

from src.common import PasswordHasher, PasswordStorage, Settings

ROCKYOU_DOWNLOAD_URL = "https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt"


def init_db(file_path: str, db_client: Redis, password_count: int = 0) -> int:
    """Return the number of password inserted in db"""
    processed = 0
    hasher = PasswordHasher()
    storage = PasswordStorage(client=db_client)

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        MofNCompleteColumn(),
    ) as progress:
        rich_task = progress.add_task("[green]Inserting in database...", total=password_count)
        # Actual work
        with open(file_path, encoding="latin-1") as file:
            for line in file:
                password = line.strip()
                prefix = hasher.prefix(password)
                storage.add_password(prefix=prefix, password=password)

                processed += 1
                progress.update(rich_task, advance=1)

    storage.flush()
    print("[green]done")
    return processed


def download_rockyou(download_file):
    with httpx.stream("GET", ROCKYOU_DOWNLOAD_URL, follow_redirects=True) as r:
        for data in r.iter_bytes():
            download_file.write(data)
    download_file.close()


if __name__ == "__main__":
    start = time.time()
    args = docopt(__doc__)
    if args.get("--download"):
        print("Initializing DB with rockyou passwords from internet")
        # Create a temporary file that is deleted automatically on program close
        download_file = tempfile.NamedTemporaryFile(delete=True, delete_on_close=False)
        download_rockyou(download_file)
        print("download complete")
        password_path = download_file.name
    elif password_path := args.get("<passwords-path>"):
        print(f"Initializing db with {password_path}")
    else:
        print("Missing arguments")
        exit(1)

    settings = Settings()
    password_count = 0
    with rich.progress.open(
        password_path,
        encoding="latin-1",
        description="[orange3]Determining password count...",
        transient=True,
    ) as file:
        for line in file:
            password_count += 1

    redis_client = Redis.from_url(str(settings.kvrocks_url))
    init_db(password_path, db_client=redis_client, password_count=password_count)
    duration = time.time() - start
    print(f"Took {duration:.2f}s")
