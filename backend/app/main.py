from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware

from .models import BookingCreate, BookingRead, BookingUpdate, HotelStay, UserRead
from .repository import TravelRepository

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "travel.db"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.repository = TravelRepository(DATA_DIR, DB_PATH)
    app.state.repository.initialize()
    yield


app = FastAPI(title="RoamReady API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_repository() -> TravelRepository:
    return app.state.repository


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the RoamReady API"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/hotels/search", response_model=list[HotelStay])
def search_hotels(name: str = Query(min_length=1, max_length=100), repository: TravelRepository = Depends(get_repository)) -> list[dict[str, object]]:
    return repository.search_stays(name)


@app.get("/api/users", response_model=list[UserRead])
def list_users(repository: TravelRepository = Depends(get_repository)) -> list[dict[str, object]]:
    return repository.list_users()


@app.get("/api/bookings", response_model=list[BookingRead])
def list_bookings(repository: TravelRepository = Depends(get_repository)) -> list[dict[str, object]]:
    return repository.list_bookings()


@app.post("/api/bookings", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, repository: TravelRepository = Depends(get_repository)) -> dict[str, object]:
    try:
        return repository.create_booking(booking.user_id, booking.trip_id, booking.guests)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.put("/api/bookings/{booking_id}", response_model=BookingRead)
def update_booking(booking_id: int, booking: BookingUpdate, repository: TravelRepository = Depends(get_repository)) -> dict[str, object]:
    try:
        return repository.update_booking(booking_id, booking.user_id, booking.guests)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.delete("/api/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, repository: TravelRepository = Depends(get_repository)) -> Response:
    if not repository.delete_booking(booking_id):
        raise HTTPException(status_code=404, detail="Booking not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
