Restaurant Management - Custom Admin + Orders
=============================================

What's included
- Contact Us page at `/contact/` with email notification and confirmation page.
- Custom Management Dashboard at `/management/` (separate from Django Admin) for users, stations, ingredients, station–ingredient assignments, and quick stats.
- Station-based architecture: `Station` and `StationIngredient` models, ingredient orders tagged with station and user location, and station selection required on creation.
- Simplified roles: admin, staff, orderer; each user belongs to a location (180 Queen, 151 Yonge, 33 Yonge).

Setup
1) Apply migrations: `python manage.py migrate`
2) Optional: set email envs for contact notifications: `ADMIN_EMAIL`, `DEFAULT_FROM_EMAIL`, and Django email backend settings as needed.
3) Environment:
   - Copy `.env.example` to `.env` and set `SECRET_KEY`, `ALLOWED_HOSTS`, and `CSRF_TRUSTED_ORIGINS`.
   - For local dev you can keep `DEBUG=True` and set `USE_SQLITE_FALLBACK=True` to avoid Postgres.
   - In production set `DEBUG=False`, provide a real `DATABASE_URL`, and remove `ALLOW_INSECURE_SECRET_KEY`.

Access
- Management Dashboard requires admin role or `accounts.admin_full_access` permission.

Notes
- Legacy `Ingredient.station` text field is still present for compatibility, but assignments should be managed via `StationIngredient`.
- Navbar shows "Management" only for admins and "Contact Us" for everyone.

Tests
- Run `python manage.py test` (set `USE_SQLITE_FALLBACK=True` if you do not have Postgres handy). 
