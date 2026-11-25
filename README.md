# ExchangeIt

A web-based currency converter built with Django, Supabase, and a Binance-inspired UI.

## Tech Stack

- **Backend:** Python 3.11+, Django 5.1.7
- **Database:** Supabase (PostgreSQL)
- **Frontend:** Django Templates, Vanilla CSS 
- **External API:** Frankfurter (exchange rates, Phase 2)

## Key Features 

- **Custom email-based authentication** — no username; email is the login identifier.
- **Role-based access control** — separate `ADMIN` and `USER` dashboards with enforced routing/isolation.
- **Profile management** — view/edit full name, contact number, and optional profile photo.

## Core Feature

The Phase 2 currency converter is available to logged-in `USER` accounts:

- **Currency Converter** (`/converter/convert/`) — choose a from/to currency and amount; rates come live from the [Frankfurter API](https://www.frankfurter.app/). Each successful conversion is saved to history.
- **Conversion History** (`/converter/history/`) — review past conversions with the rate used, and delete records you no longer need.
- **Favorite Pairs** (`/converter/favorites/`) — save frequently used pairs, quick-convert them, or delete them.

Unsupported pairs or API failures show a friendly error instead of saving a record.

## Phase 3: Hardening

- **Custom 404 and 500 error pages** for a consistent dark-mode experience when something goes wrong.
- **Full CRUD for favorite pairs** — add, view, edit, and delete saved pairs.
- **Delete confirmations** on history and favorite deletions to prevent accidental data loss.
- **Transaction atomicity for all database writes**, so a failed operation cannot leave partial records.
- **10 passing unit tests** covering access control, validation, and models.

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

### 6. Seed currencies

```bash
python manage.py seed_currencies
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the server

```bash
python manage.py runserver_plus
```

On Windows, `runserver_plus` uses Werkzeug's stat poller for reliable hot reload (configured in `settings.py`).

Open http://127.0.0.1:8000/register/ to register, or http://127.0.0.1:8000/login/ to log in.

## Running Tests

```bash
python manage.py test --keepdb
```

`--keepdb` is recommended: it reuses the existing test database and avoids Supabase pooler connection timeouts during setup and teardown.

## Project Structure

- `accounts/` — custom `User` model/manager, auth forms and views, role decorators, profile logic, migrations.
- `converter/` — currency models, conversion/favorite forms and views, Frankfurter client, seed command, migrations.
- `exchangeit/` — Django project package: settings, URL configuration, WSGI/ASGI entrypoints.
- `templates/` — shared `base.html` plus auth, dashboard, and profile templates.
- `static/css/` — `tokens.css` (DESIGN.md custom properties) and `app.css` (hand-written components).


