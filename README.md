# Pocket Ledger – Personal Expense Tracker (Django + PostgreSQL)

A responsive expense tracker built with **Python Django** and **PostgreSQL**. Add income and expenses, see your balance update instantly, filter and search your history, and review monthly spending.

## Features

- Dashboard: total income, total expenses and current balance (updates on every add, edit or delete)
- Add-transaction form: title, amount, type (income / expense), category, date
- Transaction history showing title, amount, category, type and date
- Delete with a confirmation dialog
- Filter: All / Income / Expenses
- Data stored in PostgreSQL through the Django ORM, plus a LocalStorage copy that shows the last saved list if the server is unreachable
- Responsive for desktop, tablet and mobile (table turns into cards on phones)
- Validation in the browser and in Django forms: no empty fields, no invalid amounts
- Empty-state message, success and error messages
- Bonus: edit, search by title, monthly expense summary
- Django admin at `/admin/` for managing records

## Tech stack

| Layer    | Technology                                   |
|----------|----------------------------------------------|
| Backend  | Python 3.10+, Django 5.1                     |
| Database | PostgreSQL via `psycopg` 3                   |
| Frontend | Django template, CSS, vanilla JavaScript     |

## Project structure

```
expense-tracker-django/
├── manage.py
├── requirements.txt
├── .env.example
├── config/                  # project settings and root URLs
└── tracker/                 # the app
    ├── models.py            # Transaction model
    ├── forms.py             # server-side validation
    ├── views.py             # page view + JSON API
    ├── urls.py
    ├── admin.py
    ├── migrations/0001_initial.py
    ├── templates/tracker/index.html
    └── static/tracker/      # style.css, app.js
```

## How to run

**Requirements:** Python 3.10+ and PostgreSQL 13+.

1. **Create a virtual environment and install packages**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Create the database**
   ```bash
   psql -U postgres -c "CREATE DATABASE expense_tracker;"
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env            # Windows: copy .env.example .env
   ```
   Edit `.env` and set `DB_PASSWORD` (and `DJANGO_SECRET_KEY`).

4. **Create the tables**
   ```bash
   python manage.py migrate
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```
   Open **http://127.0.0.1:8000**

6. *(Optional)* create an admin user: `python manage.py createsuperuser`, then visit `/admin/`.

If Django reports model changes that have no migration, run `python manage.py makemigrations` once and then `migrate` again.

## API

All endpoints return JSON and require the CSRF token that the page supplies automatically.

| Method | Endpoint                    | Description           |
|--------|-----------------------------|-----------------------|
| GET    | `/api/transactions/`        | List transactions     |
| POST   | `/api/transactions/`        | Create a transaction  |
| PUT    | `/api/transactions/<id>/`   | Update a transaction  |
| DELETE | `/api/transactions/<id>/`   | Delete a transaction  |

Example body for POST / PUT:

```json
{ "title": "Lunch", "amount": "12.50", "type": "expense", "category": "Food", "date": "2026-11-09" }
```

## Notes

- Amounts use `DecimalField(max_digits=12, decimal_places=2)`, and the database has a CHECK constraint so an amount can never be zero or negative.
- Change the display currency with `CURRENCY` at the top of `static/tracker/app.js`.
- Hosted databases (Neon, Supabase, Render): set `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` and `DB_SSLMODE=require`.
- For production set `DJANGO_DEBUG=False`, a strong `DJANGO_SECRET_KEY`, your domain in `DJANGO_ALLOWED_HOSTS`, and run `python manage.py collectstatic`.
