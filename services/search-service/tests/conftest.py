import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_es():
    mock = AsyncMock()
    mock.search = AsyncMock()
    mock.index = AsyncMock()
    mock.update = AsyncMock()
    mock.delete = AsyncMock()
    return mock