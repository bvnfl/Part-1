import csv
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterator


class TravelRepository:
    def __init__(self, data_dir: Path, db_path: Path) -> None:
        self.data_dir = data_dir
        self.db_path = db_path

    def _read_csv(self, name: str) -> list[dict[str, str]]:
        with (self.data_dir / name).open(encoding="utf-8-sig", newline="") as source:
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
                CREATE TABLE IF NOT EXISTS hotels (
                    hotel_id TEXT PRIMARY KEY, hotel_name TEXT NOT NULL, city TEXT NOT NULL,
                    state TEXT NOT NULL, nightly_rate_usd NUMERIC NOT NULL
                );
                CREATE TABLE IF NOT EXISTS trips (
                    trip_id TEXT PRIMARY KEY, hotel_id TEXT NOT NULL REFERENCES hotels(hotel_id),
                    trip_name TEXT NOT NULL, check_in TEXT NOT NULL, check_out TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY, display_name TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS bookings (
                    booking_id TEXT PRIMARY KEY, user_id TEXT NOT NULL REFERENCES users(user_id),
                    trip_id TEXT NOT NULL REFERENCES trips(trip_id), booked_on TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('confirmed', 'cancelled'))
                );
            """)
            for table, filename, columns in (
                ("hotels", "hotels.csv", "hotel_id, hotel_name, city, state, nightly_rate_usd"),
                ("trips", "trips.csv", "trip_id, hotel_id, trip_name, check_in, check_out"),
                ("users", "users.csv", "user_id, display_name"),
                ("bookings", "bookings.csv", "booking_id, user_id, trip_id, booked_on, status"),
            ):
                if connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0:
                    rows = self._read_csv(filename)
                    keys = columns.replace(" ", "").split(",")
                    placeholders = ", ".join(f":{key}" for key in keys)
                    connection.executemany(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", rows)

    def search_stays(self, query: str) -> list[dict[str, Any]]:
        term = f"%{query.strip().casefold()}%"
        with self._connect() as connection:
            rows = connection.execute("""
                SELECT h.*, t.trip_id, t.trip_name, t.check_in, t.check_out
                FROM hotels h JOIN trips t ON t.hotel_id = h.hotel_id
                WHERE lower(h.hotel_name) LIKE ? OR lower(h.city) LIKE ?
                ORDER BY t.check_in, t.trip_id
            """, (term, term)).fetchall()
        stays = []
        for item in map(dict, rows):
            nights = (datetime.fromisoformat(item["check_out"]) - datetime.fromisoformat(item["check_in"])).days
            stays.append({**item, "nights": nights, "stay_price_usd": nights * float(item["nightly_rate_usd"])})
        return stays

    def list_users(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            return [dict(row) for row in connection.execute("SELECT * FROM users ORDER BY user_id")]

    def list_bookings(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            return [dict(row) for row in connection.execute("""
                SELECT b.*, u.display_name AS traveler_name, t.trip_name, h.hotel_name,
                       h.city, h.state, t.check_in, t.check_out
                FROM bookings b
                JOIN users u ON u.user_id = b.user_id
                JOIN trips t ON t.trip_id = b.trip_id
                JOIN hotels h ON h.hotel_id = t.hotel_id
                ORDER BY b.booking_id DESC
            """)]

    def _validate(self, user_id: str, trip_id: str) -> None:
        with self._connect() as connection:
            if connection.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)).fetchone() is None:
                raise ValueError("The selected traveler does not exist")
            if connection.execute("SELECT 1 FROM trips WHERE trip_id = ?", (trip_id,)).fetchone() is None:
                raise ValueError("The selected stay does not exist")

    def create_booking(self, user_id: str, trip_id: str) -> dict[str, Any]:
        self._validate(user_id, trip_id)
        with self._connect() as connection:
            values = [int(row[0][1:]) for row in connection.execute("SELECT booking_id FROM bookings") if str(row[0]).startswith("B") and str(row[0])[1:].isdigit()]
            booking_id = f"B{max(values, default=0) + 1:03d}"
            connection.execute(
                "INSERT INTO bookings(booking_id, user_id, trip_id, booked_on, status) VALUES (?, ?, ?, ?, 'confirmed')",
                (booking_id, user_id, trip_id, date.today().isoformat()),
            )
        return next(item for item in self.list_bookings() if item["booking_id"] == booking_id)

    def update_booking(self, booking_id: str, user_id: str, status: str) -> dict[str, Any]:
        with self._connect() as connection:
            row = connection.execute("SELECT trip_id FROM bookings WHERE booking_id = ?", (booking_id,)).fetchone()
        if row is None:
            raise LookupError("Booking not found")
        self._validate(user_id, row["trip_id"])
        with self._connect() as connection:
            connection.execute("UPDATE bookings SET user_id = ?, status = ? WHERE booking_id = ?", (user_id, status, booking_id))
        return next(item for item in self.list_bookings() if item["booking_id"] == booking_id)

    def delete_booking(self, booking_id: str) -> bool:
        with self._connect() as connection:
            return connection.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,)).rowcount > 0
