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


def init_db(file_path: str):
    pass


if __name__ == "__main__":
    args = docopt(__doc__)
    if args.get("--download"):
        print("not implemented yet")
        exit(0)
    elif password_path := args.get("<passwords-path>"):
        print(f"Initializing db with {password_path}")
        init_db(password_path)
    # else docopt will show help
