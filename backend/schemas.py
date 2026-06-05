from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Auth
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# Location
class LocationOut(BaseModel):
    id: int
    name: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    bg_image: str

    class Config:
        from_attributes = True

# Scene
class SceneOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    preview_image: str
    bg_image: str

    class Config:
        from_attributes = True

# Sound
class SoundOut(BaseModel):
    id: int
    name: str
    file_path: str
    weather_condition: Optional[str]
    location_id: Optional[int]
    scene_id: Optional[int]

    class Config:
        from_attributes = True

# Music
class MusicTrackOut(BaseModel):
    id: int
    title: str
    file_path: str
    mood_tag: Optional[str]

    class Config:
        from_attributes = True

# Weather
class WeatherOut(BaseModel):
    time_of_day: str
    weather_code: int
    is_raining: bool
    is_snowing: bool
    is_foggy: bool
    temperature: Optional[float]

# Favorites
class FavoriteCreate(BaseModel):
    location_id: Optional[int] = None
    scene_id: Optional[int] = None

class FavoriteOut(BaseModel):
    id: int
    user_id: int
    location_id: Optional[int]
    scene_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

# Settings
class SettingsUpdate(BaseModel):
    last_location_id: Optional[int] = None
    last_scene_id: Optional[int] = None
    last_track_id: Optional[int] = None
    volume_sounds: Optional[float] = None
    volume_music: Optional[float] = None

class SettingsOut(BaseModel):
    last_location_id: Optional[int]
    last_scene_id: Optional[int]
    last_track_id: Optional[int]
    volume_sounds: float
    volume_music: float

    class Config:
        from_attributes = True
