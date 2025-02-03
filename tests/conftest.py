import os
from unittest import mock

import pytest
from redis import Redis
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from src.api.dependencies import get_settings, get_settings_cached
from src.api.main import app
from src.common import PasswordStorage

KVROCKS_IMAGE = "apache/kvrocks:2.11.0"


@pytest.fixture(scope="session", autouse=True)
def settings():  # disable the cache on settings, so it'll be reloaded everytime
    app.dependency_overrides[get_settings_cached] = get_settings
    try:
        yield get_settings  # to give tests access to settings easily if needed
    finally:
        app.dependency_overrides = {}


@pytest.fixture(scope="session")
def _kvrocks() -> Redis:
    with DockerContainer(image=KVROCKS_IMAGE).with_exposed_ports(6666) as kvrocks_container:
        wait_for_logs(kvrocks_container, "Ready to accept connections")
        host = kvrocks_container.get_container_host_ip()
        port = kvrocks_container.get_exposed_port(6666)

        with mock.patch.dict(os.environ, {"KVROCKS_URL": f"redis://{host}:{port}"}):
            yield Redis(host=host, port=port)


@pytest.fixture()
def kvrocks(_kvrocks) -> Redis:
    try:
        yield _kvrocks
    finally:
        # Clean up keys after the test is done
        for key in _kvrocks.keys():
            _kvrocks.delete(key)


@pytest.fixture
def password_storage(kvrocks):
    password_storage_ = PasswordStorage(client=kvrocks)
    password_storage_.PIPELINE_MAX_SIZE = 1  # so we don't have to flush in our test
    yield password_storage_
