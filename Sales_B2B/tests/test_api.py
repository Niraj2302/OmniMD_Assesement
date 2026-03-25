import pytest
from httpx import AsyncClient, ASGITransport
from api.main import app, results_db


@pytest.mark.asyncio
async def test_ingest_event_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {"prospect_id": "1", "event_trigger": "test_run"}
        response = await ac.post("/events/ingest", json=payload)

    assert response.status_code == 200
    assert "1" in results_db


@pytest.mark.asyncio
async def test_get_prospect_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/prospects/999")
    assert response.status_code == 404