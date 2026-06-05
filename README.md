# Virtual Window

## Быстрый старт

### 1. Создать базу данных PostgreSQL

```bash
psql -U postgres
CREATE DATABASE virtual_window;
\q
```

Или через pgAdmin / DBeaver — просто создай БД с именем `virtual_window`.

Если нужен другой пользователь / пароль — задай переменную окружения:
```bash
export DATABASE_URL="postgresql://USER:PASSWORD@localhost:5432/virtual_window"
```

### 2. Запустить бекенд

```bash
cd backend
pip install -r requirements.txt

# При проблемах с библиотекой bcrypt скачать её можно с зеркала:
# pip install bcrypt==4.0.1 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# Запустить сервер (таблицы создадутся автоматически)
uvicorn main:app --reload

# Заполнить БД начальными данными
python seed.py
```

Бекенд работает на http://localhost:8000  
Документация API: http://localhost:8000/docs

### 3. Запустить фронтенд

```bash
cd frontend
npm install
npm run dev
```

Фронтенд работает на http://localhost:5173

---

## Структура проекта

```
virtual-window/
├── backend/                      Python / FastAPI
│   ├── main.py                   Точка входа, регистрация роутеров
│   ├── database.py               SQLAlchemy engine и сессия
│   ├── models.py                 Модели БД (7 таблиц)
│   ├── schemas.py                Pydantic-схемы запросов/ответов
│   ├── auth_utils.py             bcrypt, JWT, get_current_user
│   ├── seed.py                   Заполнение БД начальными данными
│   ├── create_db.sql             SQL для создания базы
│   ├── requirements.txt          Зависимости Python
│   ├── routers/
│   │   ├── auth.py               POST /auth/register|login|logout|me
│   │   ├── locations.py          GET /locations, /locations/{id}
│   │   ├── scenes.py             GET /scenes, /scenes/{id}
│   │   ├── sounds.py             GET /sounds?location_id=|scene_id=
│   │   ├── music.py              GET /music
│   │   ├── weather.py            GET /weather/{location_id} → Open-Meteo
│   │   ├── favorites.py          GET|POST|DELETE /favorites
│   │   └── settings.py           GET|PUT /settings
│   └── static/
│       ├── images/               Фоны локаций и превью сцен (.jpg/.gif)
│       ├── sounds/               Звуки окружения (.mp3)
│       └── music/                Фоновая музыка (.mp3)
│
└── frontend/                     React / Vite
    ├── index.html
    ├── vite.config.js
    └── src/
        ├── main.jsx              Точка входа React
        ├── App.jsx               Корневой компонент, сборка оверлеев
        ├── App.css
        ├── styles/
        │   └── globals.css       CSS-переменные, glassmorphism, keyframes
        ├── api/
        │   ├── client.js         Axios с withCredentials
        │   └── endpoints.js      Все API-функции
        ├── context/
        │   └── AppContext.jsx    React Context — весь глобальный стейт
        └── components/
            ├── Header/           Glassmorphism-шапка, кнопки управления
            ├── Window/           Полноэкранный фон, подпись локации
            ├── WeatherOverlay/   CSS-анимации дождя / снега / тумана
            ├── LocationDropdown/ Дропдаун выбора локации и сцены
            ├── SoundPanel/       Плеер музыки + переключатели звуков
            ├── BreathingOverlay/ Дыхательная гимнастика 4-7-8
            ├── Auth/             Форма входа и регистрации
            └── UserPanel/        Профиль, избранное, выход
```

## ТЕСТЫ

### backend

```
cd backend
pip install pytest pytest-asyncio httpx pytest-cov

# With warnings
python -m pytest tests/ -v

# Without warnings
python -m pytest tests/ -v --disable-warnings
```

### frontend
```
npm install --save-dev vitest @vitest/coverage-v8 @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
npx vitest run
```