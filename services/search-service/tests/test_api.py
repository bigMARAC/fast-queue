import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app
from unittest.mock import patch


@pytest.mark.asyncio
async def test_search_endpoint_success(mock_es):
    mock_es.search.return_value = {
        "hits": {
            "hits": [{"_source": {"display_name": "Maracbot", "queue_title": "Fila 1"}}]
        }
    }

    transport = ASGITransport(app=app)

    with patch("src.main.es", mock_es):
        async with AsyncClient(
            transport=transport, base_url="http://test", follow_redirects=True
        ) as ac:
            response = await ac.get("/v1/search?q=marac")

    assert response.status_code == 200
