import xxhash
from redis import Redis

from src.common import Password, Prefix


class PasswordHasher:
    def __init__(self):
        pass

    @staticmethod
    def prefix(password: Password) -> Prefix:
        """Return the prefix (first 5 chars) of the password's hash"""
        xxh32 = xxhash.xxh32()
        xxh32.update(password.encode())
        digest = xxh32.hexdigest()
        return digest[:5]


class PasswordStorage:
    PIPELINE_MAX_SIZE = 200

    def __init__(self, client: Redis):
        self.client = client
        self._pipe = client.pipeline(transaction=False)
        self._pipe_size = 0

    def add_password(self, *, prefix: Prefix, password: Password):
        self._pipe.sadd(prefix, password)
        self._pipe_size += 1
        if self._pipe_size == self.PIPELINE_MAX_SIZE:
            self.flush()

    def get_passwords(self, prefix: Prefix) -> set[Password]:
        passwords_as_bytes = self.client.smembers(prefix)
        return {password.decode() for password in passwords_as_bytes}

    def flush(self):
        self._pipe.execute()
        self._pipe_size = 0
