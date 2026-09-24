from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.repository import TravelRepository


def test_search_and_booking_crud(tmp_path: Path) -> None:
    repository = TravelRepository(Path(__file__).parents[1] / "data", tmp_path / "test.db")
    repository.initialize()
    with TestClient(app) as client:
        app.state.repository = repository
        assert len(client.get("/api/hotels/search", params={"name": "harbor"}).json()) == 2
        assert client.get("/api/hotels/search", params={"name": "missing"}).json() == []
        created = client.post("/api/bookings", json={"user_id": 3, "trip_id": 104, "guests": 2})
        assert created.status_code == 201
        booking_id = created.json()["booking_id"]
        updated = client.put(f"/api/bookings/{booking_id}", json={"user_id": 1, "guests": 3})
        assert updated.json()["guests"] == 3
        assert client.delete(f"/api/bookings/{booking_id}").status_code == 204
        assert all(item["booking_id"] != booking_id for item in client.get("/api/bookings").json())
