from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class HotelStay(BaseModel):
    hotel_id: int
    hotel_name: str
    city: str
    country: str
    trip_id: int
    check_in: date
    check_out: date
    price_per_night: Decimal
    rooms_available: int


class UserRead(BaseModel):
    user_id: int
    name: str
    email: str


class BookingCreate(BaseModel):
    user_id: int
    trip_id: int
    guests: int = Field(ge=1, le=8)


class BookingUpdate(BaseModel):
    user_id: int
    guests: int = Field(ge=1, le=8)


class BookingRead(BaseModel):
    booking_id: int
    user_id: int
    traveler_name: str
    trip_id: int
    hotel_name: str
    city: str
    check_in: date
    check_out: date
    guests: int
    status: str
