import pytest
from redis import Redis
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

KVROCKS_IMAGE = "apache/kvrocks:2.11.0"


@pytest.fixture(scope="session")
def _kvrocks() -> Redis:
    with DockerContainer(image=KVROCKS_IMAGE).with_exposed_ports(6666) as kvrocks_container:
        wait_for_logs(kvrocks_container, "Ready to accept connections")
        host = kvrocks_container.get_container_host_ip()
        port = kvrocks_container.get_exposed_port(6666)

        yield Redis(host=host, port=port)

@pytest.fixture()
def kvrocks(_kvrocks) -> Redis:
    try:
        yield _kvrocks
    finally:
        # Clean up keys after the test is done
        for key in _kvrocks.keys():
            _kvrocks.delete(key)