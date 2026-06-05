from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import httpx

import models
import schemas
from database import get_db

router = APIRouter(prefix="/weather", tags=["weather"])

# https://open-meteo.com/en/docs#weathervariables
RAIN_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}
SNOW_CODES = {71, 73, 75, 77, 85, 86}
FOG_CODES  = {45, 48}

def parse_dt(s: str) -> datetime:
    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {s}")

def compute_time_of_day(now: datetime, sunrise: datetime, sunset: datetime) -> str:
    from datetime import timedelta
    if now < sunrise - timedelta(minutes=60) or now > sunset + timedelta(minutes=60):
        return "night"
    if now < sunrise + timedelta(minutes=120):
        return "morning"
    if now < sunset - timedelta(minutes=90):
        return "day"
    return "evening"

@router.get("/{location_id}", response_model=schemas.WeatherOut)
async def get_weather(location_id: int, db: Session = Depends(get_db)):
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={loc.latitude}&longitude={loc.longitude}"
        f"&current_weather=true"
        f"&daily=sunrise,sunset"
        f"&timezone=auto"
    )

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Weather API error: {e}")

    cw = data["current_weather"]
    weather_code: int = cw["weathercode"]
    temperature: float = cw["temperature"]

    now_str: str = cw["time"]
    sunrise_str: str = data["daily"]["sunrise"][0]
    sunset_str: str = data["daily"]["sunset"][0]

    now = parse_dt(now_str)
    sunrise = parse_dt(sunrise_str)
    sunset = parse_dt(sunset_str)

    time_of_day = compute_time_of_day(now, sunrise, sunset)

    return schemas.WeatherOut(
        time_of_day=time_of_day,
        weather_code=weather_code,
        is_raining=weather_code in RAIN_CODES,
        is_snowing=weather_code in SNOW_CODES,
        is_foggy=weather_code in FOG_CODES,
        temperature=temperature,
    )