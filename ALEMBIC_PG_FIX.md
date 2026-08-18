# Alembic PostgreSQL Driver Fix

## Problem

When running:

```powershell
alembic revision --autogenerate -m "create users and platform_identities"
```

Alembic failed with:

```text
ModuleNotFoundError: No module named 'psycopg2'
```

## Cause

The first failure was caused by `alembic/env.py` passing a `DATABASE_URL` containing `%40` (URL-encoded `@`) into `config.set_main_option(...)`.
`configparser` treats `%` as interpolation syntax, so the URL was rejected before Alembic could even connect.

## First Fix

Updated `alembic/env.py` to escape `%` characters in the database URL before calling `config.set_main_option(...)`:

```python
db_url = os.getenv("DATABASE_URL")
if db_url is None:
    raise RuntimeError("DATABASE_URL environment variable is not set")
config.set_main_option("sqlalchemy.url", db_url.replace("%", "%%"))
```

## Second Fix

Installed the missing sync driver in the virtual environment:

```powershell
pip install psycopg2-binary
```

This provides the `psycopg2` module required by SQLAlchemy when Alembic creates the migration engine.

## Notes

- The application can still use `postgresql+asyncpg://` for async behavior.
- Alembic `env.py` in this project was not configured for async migrations, so the sync driver is required for the migration command.
