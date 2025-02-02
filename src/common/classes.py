from redis import Redis

from src.common import Password, Prefix


class PasswordStorage:
    def __init__(self, client: Redis):
        self.client = client

    def add_password(self, *, prefix: Prefix, password: Password):
        self.client.sadd(prefix, password)

    def get_passwords(self, prefix: Prefix) -> set[Password]:
        passwords_as_bytes = self.client.smembers(prefix)
        return {password.decode() for password in passwords_as_bytes}
