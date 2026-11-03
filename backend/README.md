# Blood Nation backend

Django 5.2 LTS on Python 3.13, managed with uv. This is the **foundation only**: no product features, models or database yet (the database, Redis and Celery come in Step 8C).

## Run it (Windows PowerShell, from this `backend` folder)

```powershell
uv sync                         # installs Python 3.13 if needed and all dependencies
uv run pytest                   # tests
uv run ruff check .             # lint
uv run ruff format --check .    # formatting check
uv run python manage.py check   # Django configuration check
uv run python manage.py runserver
```

Then open http://127.0.0.1:8000/health/ in a browser. It should show `{"status": "ok", ...}`.

## Settings

| Module | Use |
|---|---|
| `config.settings.local` | Developer computer (default for `manage.py`) |
| `config.settings.test` | Automated tests |
| `config.settings.staging` | Staging. Needs `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`. |
| `config.settings.production` | Production. Same rules. Fails to start if a required value is missing. |

Names of environment variables are listed in the root `.env.example`. Never commit a real `.env`.

## Layout

`config/` holds settings and URLs. `apps/` holds the Django apps; today only `apps/core` (the health page). Future modules (identity, consent, donors and so on) will be added under `apps/` when they are approved.
