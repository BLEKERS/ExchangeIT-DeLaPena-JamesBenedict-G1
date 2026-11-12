# Phase 1 — Account Feature Notes

## What was built

- **Project scaffold:** Django project `exchangeit` + `accounts` app, `requirements.txt` (Django 5.x, psycopg2-binary, python-decouple, dj-database-url, Pillow), `.env.example`, settings reading `.env` via `python-decouple` and `dj-database-url`.
- **Custom User (`accounts.User`):** `AbstractBaseUser + PermissionsMixin` (no `username`), email as `USERNAME_FIELD`, `REQUIRED_FIELDS = ["full_name"]`; fields `email` (unique, BR-01), `full_name`, `role` (`USER`/`ADMIN`, BR-02), optional `contact_number`, optional `profile_photo`, `is_active`, `is_staff`, `created_at`; custom `UserManager` with `create_user`/`create_superuser` (email + password, BR-03). `save()` forces `role='ADMIN'` when `is_staff` or `is_superuser`.
- **Authentication & role routing:** registration (required/valid/unique email, password match, min length 8, hashed via Django auth), login by email, POST-only logout, `post_login` routing (`ADMIN`/superuser → `/admin/dashboard/`, else `/dashboard/`), messages framework for success/error.
- **Access control:** `@login_required` on dashboards/profile; `@user_required` (only `role=='USER'` and not superuser; admins/superusers redirected to admin dashboard); `@admin_required` (`role=='ADMIN'` or superuser). Users can view/edit only their own profile.
- **Profiles:** profile view + edit (full name, contact number, optional photo via Pillow); email/role are not editable.
- **Design system:** hand-written CSS only (no Tailwind/Bootstrap/other frameworks), built from `DESIGN.md` tokens in `static/css/tokens.css` and components in `static/css/app.css` (`.btn-primary`, `.input-dark`/`.input-light`, `.card-dark`/`.card-light`, `.nav-dark`, `.footer-light`, typography classes, token-styled messages). Google Fonts: Inter (BinanceNova fallback) and IBM Plex Sans (BinancePlex fallback).
- **Templates:** `base.html` + auth pages (dark), user/admin dashboards (dark, `.card-dark`), profile view/edit (light transactional mode).

## Run from scratch

```bash
# 1. Create/activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
# Copy .env.example to .env and fill in real values (DATABASE_URL, SECRET_KEY, DEBUG, ALLOWED_HOSTS)

# 4. Migrate database
python manage.py migrate

# 5. Create admin user (interactive; email is the login identifier)
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver
```

Open http://127.0.0.1:8000/register/ to start, or http://127.0.0.1:8000/login/.

## Notes for the grader / instructor

- **Database is hosted on Supabase PostgreSQL.** No SQLite is used anywhere (settings only reads `DATABASE_URL`).
- **`DESIGN.md` is the single source of truth for styling.** Colors, fonts, radii, spacing, and components come only from its tokens; there is exactly one brand accent (`#fcd535`), no CSS frameworks, and no invented design values.
- **`DIRECT_URL` in `.env.example` is commented out and not wired into `settings.py`.** It exists only for one-off migration troubleshooting (direct Supabase host); the app always uses `DATABASE_URL` (session pooler, port 5432).
- **Scope is Phase 1 only:** account feature (register → login → role-routed dashboard → profile view/edit). The currency converter, history, favorites, reports, and admin currency management are intentionally not built yet.
- **Landing page (`/`) is intentionally left blank for Phase 2.** The root URL does not map to a view yet; use `/register/` or `/login/`.
