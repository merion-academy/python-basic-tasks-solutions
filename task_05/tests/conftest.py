import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get", autospec=True)
