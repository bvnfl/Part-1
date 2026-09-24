from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class HotelStay(BaseModel):
    hotel_id: str
    hotel_name: str
    city: str
    state: str
    trip_id: str
    trip_name: str
    check_in: date
    check_out: date
    nights: int
    nightly_rate_usd: Decimal
    stay_price_usd: Decimal


class UserRead(BaseModel):
    user_id: str
    display_name: str


class BookingCreate(BaseModel):
    user_id: str
    trip_id: str


class BookingUpdate(BaseModel):
    user_id: str
    status: Literal["confirmed", "cancelled"]


class BookingRead(BaseModel):
    booking_id: str
    user_id: str
    traveler_name: str
    trip_id: str
    trip_name: str
    hotel_name: str
    city: str
    state: str
    check_in: date
    check_out: date
    booked_on: date
    status: str
