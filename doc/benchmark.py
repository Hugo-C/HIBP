import hashlib
import random
import string

import xxhash  # install with pip install xxhash


def random_password(length):
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def hash_sha512(password):
    m = hashlib.sha512()
    m.update(password.encode())
    return m.hexdigest()


def hash_md5(password):
    m = hashlib.md5()
    m.update(password.encode())
    return m.hexdigest()


def hash_xxh(password):
    m = xxhash.xxh32()
    m.update(password.encode())
    return m.hexdigest()


if __name__ == "__main__":
    password = random_password(15)
    print(hash_xxh(password))
