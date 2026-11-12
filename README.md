# ExchangeIt

A web-based currency converter built with Django, Supabase, and a Binance-inspired UI.

## Tech Stack

- **Backend:** Python 3.11+, Django 5.1.7
- **Database:** Supabase (PostgreSQL)
- **Frontend:** Django Templates, Vanilla CSS (strictly following `DESIGN.md` tokens, no CSS frameworks)
- **External API:** Frankfurter (exchange rates, Phase 2)

## Key Features (Phase 1 Complete)

- **Custom email-based authentication** — no username; email is the login identifier.
- **Role-based access control** — separate `ADMIN` and `USER` dashboards with enforced routing/isolation.
- **Profile management** — view/edit full name, contact number, and optional profile photo; light-mode transactional UI vs. dark product UI per `DESIGN.md`.
- **Strict adherence to `DESIGN.md`** — colors, typography, radii, spacing, and components come only from its token system.

## Local Setup

### Prerequisites

- Python 3.11+
- Git

### 1. Clone the repo

```bash
git clone https://github.com/BLEKERS/ExchangeIT-DeLaPena-JamesBenedict-G1.git
cd ExchangeIT-DeLaPena-JamesBenedict-G1
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment variables

Copy `.env.example` to `.env` and fill in your Supabase `DATABASE_URL` and `SECRET_KEY` (plus `DEBUG` and `ALLOWED_HOSTS` as needed).

```bash
cp .env.example .env
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/register/ to register, or http://127.0.0.1:8000/login/ to log in.

## Project Structure

- `accounts/` — custom `User` model/manager, auth forms and views, role decorators, profile logic, migrations.
- `exchangeit/` — Django project package: settings, URL configuration, WSGI/ASGI entrypoints.
- `templates/` — shared `base.html` plus auth, dashboard, and profile templates.
- `static/css/` — `tokens.css` (DESIGN.md custom properties) and `app.css` (hand-written components).

## Phase 2 Roadmap

- Currency converter implementation (Frankfurter API integration, swap, refresh).
- Conversion history tracking (save every conversion, view/search/filter).
- Favorite currency pairs (add/edit/delete).
