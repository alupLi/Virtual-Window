import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def seed_locations():
    if db.query(models.Location).count():
        print("Locations already seeded, skipping.")
        return

    locations = [
        models.Location(name="Норвежские фьорды",    country="Норвегия",      latitude=61.1,  longitude=6.9,    timezone="Europe/Oslo",          bg_image="/static/images/norway_fjords.jpg"),
        models.Location(name="Лес Якусима",           country="Япония",         latitude=30.3,  longitude=130.5,  timezone="Asia/Tokyo",           bg_image="/static/images/japan_yakushima.jpeg"),
        models.Location(name="Исландское плато",      country="Исландия",       latitude=64.9,  longitude=-18.1,  timezone="Atlantic/Reykjavik",   bg_image="/static/images/iceland_plateau.jpg"),
        models.Location(name="Тоскана",               country="Италия",         latitude=43.3,  longitude=11.3,   timezone="Europe/Rome",          bg_image="/static/images/tuscany.jpg"),
        models.Location(name="Шотландские горы",      country="Шотландия",      latitude=57.0,  longitude=-4.2,   timezone="Europe/London",        bg_image="/static/images/scotland_highlands.jpg"),
        models.Location(name="Аляска, тайга",         country="США",            latitude=64.2,  longitude=-153.0, timezone="America/Anchorage",    bg_image="/static/images/alaska_taiga.jpg"),
        models.Location(name="Амазония",              country="Бразилия",       latitude=-3.4,  longitude=-62.2,  timezone="America/Manaus",       bg_image="/static/images/amazon_jungle.jpg"),
        models.Location(name="Патагония",             country="Аргентина",      latitude=-50.9, longitude=-73.1,  timezone="America/Argentina/Rio_Gallegos", bg_image="/static/images/patagonia.jpg"),
        models.Location(name="Лапландия",             country="Финляндия",      latitude=68.9,  longitude=27.0,   timezone="Europe/Helsinki",      bg_image="/static/images/lapland.jpg"),
        models.Location(name="Побережье Новой Зеландии", country="Новая Зеландия", latitude=-45.0, longitude=168.6, timezone="Pacific/Auckland",   bg_image="/static/images/new_zealand_coast.jpg"),
    ]
    db.add_all(locations)
    db.commit()
    print(f"Added {len(locations)} locations.")
    return locations


def seed_scenes():
    if db.query(models.Scene).count():
        print("Scenes already seeded, skipping.")
        return

    scenes = [
        models.Scene(name="Сказочный лес",              description="Древний лес, где деревья светятся изнутри",         preview_image="/static/images/scene_forest_preview.jpg",    bg_image="/static/images/scene_forest.gif"),
        models.Scene(name="Подводный мир",               description="Бездонный океан с мерцающими медузами",              preview_image="/static/images/scene_ocean_preview.jpg",     bg_image="/static/images/scene_ocean.gif"),
        models.Scene(name="Космическая станция",         description="Иллюминатор орбитальной станции над Землёй",        preview_image="/static/images/scene_space_preview.jpg",     bg_image="/static/images/scene_space.gif"),
        models.Scene(name="Облачный город",              description="Город на облаках в золотом свете заката",           preview_image="/static/images/scene_clouds_preview.jpg",    bg_image="/static/images/scene_clouds.gif"),
        models.Scene(name="Древний храм в джунглях",    description="Заброшенный храм, поглощённый тропическими лианами", preview_image="/static/images/scene_temple_preview.jpg",    bg_image="/static/images/scene_temple.gif"),
    ]
    db.add_all(scenes)
    db.commit()
    print(f"Added {len(scenes)} scenes.")
    return scenes


def seed_sounds():
    if db.query(models.Sound).count():
        print("Sounds already seeded, skipping.")
        return

    locs = {loc.name: loc.id for loc in db.query(models.Location).all()}
    scns = {s.name: s.id for s in db.query(models.Scene).all()}

    sounds = [
        # Universal weather sounds
        models.Sound(name="Дождь",              file_path="/static/sounds/rain.mp3",        weather_condition="rain"),
        models.Sound(name="Гроза",              file_path="/static/sounds/thunder.mp3",     weather_condition="rain"),
        models.Sound(name="Метель",             file_path="/static/sounds/blizzard.mp3",    weather_condition="snow"),
        models.Sound(name="Ветер",              file_path="/static/sounds/wind.mp3",        weather_condition="fog"),

        # Location-specific sounds
        models.Sound(name="Птицы леса",         file_path="/static/sounds/birds_forest.mp3",    location_id=locs.get("Лес Якусима")),
        models.Sound(name="Морской прибой",     file_path="/static/sounds/ocean_waves.mp3",     location_id=locs.get("Побережье Новой Зеландии")),
        models.Sound(name="Горный ветер",       file_path="/static/sounds/mountain_wind.mp3",   location_id=locs.get("Шотландские горы")),
        models.Sound(name="Тропические птицы", file_path="/static/sounds/tropical_birds.mp3",  location_id=locs.get("Амазония")),
        models.Sound(name="Хвойный лес",        file_path="/static/sounds/pine_forest.mp3",     location_id=locs.get("Лапландия")),
        models.Sound(name="Цикады",             file_path="/static/sounds/cicadas.mp3",          location_id=locs.get("Тоскана")),

        # Scene sounds
        models.Sound(name="Мистический лес",    file_path="/static/sounds/mystic_forest.mp3",   scene_id=scns.get("Сказочный лес")),
        models.Sound(name="Подводное эхо",      file_path="/static/sounds/underwater.mp3",       scene_id=scns.get("Подводный мир")),
        models.Sound(name="Космос",             file_path="/static/sounds/space_hum.mp3",        scene_id=scns.get("Космическая станция")),
        models.Sound(name="Ветер в облаках",    file_path="/static/sounds/cloud_wind.mp3",       scene_id=scns.get("Облачный город")),
        models.Sound(name="Джунгли ночью",      file_path="/static/sounds/jungle_night.mp3",     scene_id=scns.get("Древний храм в джунглях")),
    ]

    db.add_all(sounds)
    db.commit()
    print(f"Added {len(sounds)} sounds.")


def seed_music():
    if db.query(models.MusicTrack).count():
        print("Music tracks already seeded, skipping.")
        return

    tracks = [
        models.MusicTrack(title="Rainy Day Lofi",       file_path="/static/music/rainy_day_lofi.mp3",       mood_tag="lofi"),
        models.MusicTrack(title="Forest Ambient",        file_path="/static/music/forest_ambient.mp3",       mood_tag="ambient"),
        models.MusicTrack(title="Late Night Study",      file_path="/static/music/late_night_study.mp3",     mood_tag="lofi"),
        models.MusicTrack(title="Deep Space",            file_path="/static/music/deep_space.mp3",           mood_tag="ambient"),
        models.MusicTrack(title="Morning Calm",          file_path="/static/music/morning_calm.mp3",         mood_tag="calm"),
        models.MusicTrack(title="Autumn Walk",           file_path="/static/music/autumn_walk.mp3",          mood_tag="lofi"),
        models.MusicTrack(title="Ocean Drift",           file_path="/static/music/ocean_drift.mp3",          mood_tag="ambient"),
    ]
    db.add_all(tracks)
    db.commit()
    print(f"Added {len(tracks)} music tracks.")


if __name__ == "__main__":
    print("Seeding database...")
    seed_locations()
    seed_scenes()
    seed_sounds()
    seed_music()
    db.close()
    print("Done!")
