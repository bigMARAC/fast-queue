import pytest
from src.worker import process_event
from unittest.mock import AsyncMock, ANY


@pytest.mark.asyncio
async def test_worker_index_new_queue(mock_es):
    mock_event = {
        "payload": {
            "op": "c",
            "after": {
                "id": 10,
                "title": "Fila Teste CDC",
                "streamer_id": "user_123",
                "streamer_name": "Maracbot",
                "status": "OPEN",
                "entry_fee": 500,
                "max_slots": 10,
            },
            "source": {"ts_ms": 1776701069514},
        }
    }

    await process_event(mock_event, mock_es)

    mock_es.index.assert_called_once_with(index="streamers", id="10", document=ANY)
