import csv
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


class TravelRepository:
    def __init__(self, data_dir: Path, db_path: Path) -> None:
        self.data_dir = data_dir
        self.db_path = db_path

    def _read_csv(self, name: str) -> list[dict[str, str]]:
        with (self.data_dir / name).open(encoding="utf-8", newline="") as source:
            return list(csv.DictReader(source))

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE);
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL REFERENCES users(user_id),
                    trip_id INTEGER NOT NULL,
                    guests INTEGER NOT NULL CHECK (guests BETWEEN 1 AND 8),
                    status TEXT NOT NULL DEFAULT 'confirmed'
                );
            """)
            if connection.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
                connection.executemany("INSERT INTO users(user_id, name, email) VALUES (:user_id, :name, :email)", self._read_csv("users.csv"))
            if connection.execute("SELECT COUNT(*) FROM bookings").fetchone()[0] == 0:
                connection.executemany(
                    "INSERT INTO bookings(booking_id, user_id, trip_id, guests, status) VALUES (:booking_id, :user_id, :trip_id, :guests, :status)",
                    self._read_csv("bookings.csv"),
                )

    def _stays(self) -> list[dict[str, Any]]:
        hotels = {row["hotel_id"]: row for row in self._read_csv("hotels.csv")}
        results: list[dict[str, Any]] = []
        for trip in self._read_csv("trips.csv"):
            hotel = hotels.get(trip["hotel_id"])
            if hotel:
                results.append({**hotel, **trip, "hotel_id": int(hotel["hotel_id"]), "trip_id": int(trip["trip_id"]), "rooms_available": int(trip["rooms_available"])})
        return results

    def search_stays(self, name: str) -> list[dict[str, Any]]:
        query = name.strip().casefold()
        return [stay for stay in self._stays() if query in str(stay["hotel_name"]).casefold()]

    def list_users(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            return [dict(row) for row in connection.execute("SELECT * FROM users ORDER BY name")]

    def list_bookings(self) -> list[dict[str, Any]]:
        stays = {stay["trip_id"]: stay for stay in self._stays()}
        with self._connect() as connection:
            rows = connection.execute("SELECT b.*, u.name AS traveler_name FROM bookings b JOIN users u ON u.user_id = b.user_id ORDER BY b.booking_id DESC").fetchall()
        return [self._booking_view(dict(row), stays) for row in rows if row["trip_id"] in stays]

    @staticmethod
    def _booking_view(row: dict[str, Any], stays: dict[int, dict[str, Any]]) -> dict[str, Any]:
        stay = stays[row["trip_id"]]
        return {**row, "hotel_name": stay["hotel_name"], "city": stay["city"], "check_in": stay["check_in"], "check_out": stay["check_out"]}

    def _validate(self, user_id: int, trip_id: int) -> None:
        if trip_id not in {stay["trip_id"] for stay in self._stays()}:
            raise ValueError("The selected stay no longer exists")
        with self._connect() as connection:
            if connection.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)).fetchone() is None:
                raise ValueError("The selected traveler does not exist")

    def create_booking(self, user_id: int, trip_id: int, guests: int) -> dict[str, Any]:
        self._validate(user_id, trip_id)
        with self._connect() as connection:
            booking_id = connection.execute("INSERT INTO bookings(user_id, trip_id, guests) VALUES (?, ?, ?)", (user_id, trip_id, guests)).lastrowid
        return next(item for item in self.list_bookings() if item["booking_id"] == booking_id)

    def update_booking(self, booking_id: int, user_id: int, guests: int) -> dict[str, Any]:
        with self._connect() as connection:
            row = connection.execute("SELECT trip_id FROM bookings WHERE booking_id = ?", (booking_id,)).fetchone()
        if row is None:
            raise LookupError("Booking not found")
        self._validate(user_id, row["trip_id"])
        with self._connect() as connection:
            connection.execute("UPDATE bookings SET user_id = ?, guests = ? WHERE booking_id = ?", (user_id, guests, booking_id))
        return next(item for item in self.list_bookings() if item["booking_id"] == booking_id)

    def delete_booking(self, booking_id: int) -> bool:
        with self._connect() as connection:
            return connection.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,)).rowcount > 0
