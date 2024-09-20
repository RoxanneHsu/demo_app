import pytest
from unittest.mock import MagicMock

@pytest.fixture(scope='function')
def mock_database():
    db = MagicMock()
    yield db
