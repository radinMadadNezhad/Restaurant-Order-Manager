Restaurant Management – Custom Admin + Contact + Stations
========================================================

What’s new
- Contact Us page at `/contact/` with email notification and confirmation page.
- Custom Management Dashboard at `/management/` (separate from Django Admin):
  - Users: view/create/edit/delete with location assignment.
  - Stations: CRUD.
  - Ingredients: CRUD.
  - Station ↔ Ingredient assignments via a dedicated page.
  - Summary panel: users per location, pending/completed ingredient orders, recent contact messages.
- Station-based architecture:
  - New models: `Station`, `StationIngredient`.
  - `IngredientOrder` carries `station` and user `location`.
  - Create Ingredient Order now requires selecting a station.
- Roles simplified; each user now belongs to a location (180 Queen, 151 Yonge, 33 Yonge).

Setup
1) Apply migrations:
   - python manage.py migrate
2) Set email envs for contact notifications (optional):
   - ADMIN_EMAIL, DEFAULT_FROM_EMAIL, and Django email backend settings as needed.

Access
- Management Dashboard requires admin role or `accounts.admin_full_access` permission.

Notes
- Legacy `Ingredient.station` is still present for compatibility, but assignments should be managed via Station ↔ Ingredient.
- Navbar shows “Management” only for admins and “Contact Us” for everyone.
