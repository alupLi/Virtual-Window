from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    favorites = relationship("UserFavorite", back_populates="user", cascade="all, delete")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String(50), nullable=False)
    bg_image = Column(String(255), nullable=False)

    sounds = relationship("Sound", back_populates="location")
    favorites = relationship("UserFavorite", back_populates="location")


class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    preview_image = Column(String(255), nullable=False)
    bg_image = Column(String(255), nullable=False)

    sounds = relationship("Sound", back_populates="scene")
    favorites = relationship("UserFavorite", back_populates="scene")


class Sound(Base):
    __tablename__ = "sounds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    file_path = Column(String(255), nullable=False)
    weather_condition = Column(String(50), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)
    scene_id = Column(Integer, ForeignKey("scenes.id", ondelete="SET NULL"), nullable=True)

    location = relationship("Location", back_populates="sounds")
    scene = relationship("Scene", back_populates="sounds")


class MusicTrack(Base):
    __tablename__ = "music_tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    file_path = Column(String(255), nullable=False)
    mood_tag = Column(String(50), nullable=True)


class UserFavorite(Base):
    __tablename__ = "user_favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="CASCADE"), nullable=True)
    scene_id = Column(Integer, ForeignKey("scenes.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "(location_id IS NOT NULL AND scene_id IS NULL) OR "
            "(location_id IS NULL AND scene_id IS NOT NULL)",
            name="check_favorite_one_target"
        ),
    )

    user = relationship("User", back_populates="favorites")
    location = relationship("Location", back_populates="favorites")
    scene = relationship("Scene", back_populates="favorites")


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    last_location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)
    last_scene_id = Column(Integer, ForeignKey("scenes.id", ondelete="SET NULL"), nullable=True)
    last_track_id = Column(Integer, ForeignKey("music_tracks.id", ondelete="SET NULL"), nullable=True)
    volume_sounds = Column(Float, default=0.7)
    volume_music = Column(Float, default=0.4)

    user = relationship("User", back_populates="settings")