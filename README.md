# RetroGen

RetroGen is a small French-language retro-gaming shop prototype built with Flask and SQLite. It was created as a high-school project to explore product catalogues, user accounts and product reviews.

## Features

- Home page and product catalogue backed by SQLite
- Product detail pages with console selection
- Registration and login with hashed passwords
- Product comments and 1–5 star ratings
- Search and category filtering in the shop

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install flask
python flask_app.py
```

Then open `http://127.0.0.1:5000`. The database is created and seeded on first import.

## Notes

This is an educational prototype. The basket and checkout screens are currently presentation-only; production concerns such as CSRF protection, migrations and a real payment flow are outside the original scope.
