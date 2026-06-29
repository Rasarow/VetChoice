# VetChoice

VetChoice is a modern Flask web platform for pet owners to discover trusted veterinarians, manage pet profiles, and publish verified reviews. The visual direction is clean, premium, white-first UI with soft purple accents inspired by Airbnb, ProDoctorov, Apple, and Stripe.

## Implemented MVP foundation

- Flask application factory with modular blueprints.
- SQLAlchemy models for users, pets, doctors, clinics, reviews, appointments, favorites, and notifications.
- Flask-Login authentication with registration/login/logout.
- Owner dashboard with pets, appointments, reviews, and notifications summary.
- Pet profile creation, editing, and detail pages.
- Specialist catalog with filters and profile pages.
- Verified review form and profile review list.
- Review verification metadata: verification type/status, moderation status, trust weight, and review documents table.
- User trust score.
- Pet profiles with photo URL, color, special marks, breed dropdown, and removed passport/weight/medical notes/allergies inputs.
- Demo seed command.
- TailwindCSS/Jinja templates and custom CSS matching the requested palette.

## Tech stack

- Python / Flask
- SQLAlchemy + Flask-Migrate
- Flask-Login / Flask-WTF / Flask-Mail
- Jinja2 templates
- TailwindCSS via CDN for MVP speed
- SQLite by default for local development; PostgreSQL-ready through `DATABASE_URL`

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
set FLASK_APP=run.py
flask seed
flask run
```

Open `http://127.0.0.1:5000`.

Demo login:

- Email: `owner@example.com`
- Password: `password123`

## PostgreSQL configuration

Set `DATABASE_URL` in `.env`:

```env
DATABASE_URL=postgresql+psycopg://vetchoice:password@localhost:5432/vetchoice
```

Then run migrations or seed data:

```bash
flask db init
flask db migrate -m "initial schema"
flask db upgrade
flask seed
```

## Roadmap alignment

### Phase 1 MVP covered

- Home page
- Specialist catalog
- Specialist profile
- User authentication
- Owner dashboard
- Pet management
- Reviews

### Suggested next steps

1. Add appointment booking calendar and available time slots.
2. Add favorites and notification center pages.
3. Add articles, Q&A, clinics, groomers, and dog trainers modules.
4. Replace Tailwind CDN with a build pipeline for production.
5. Add S3-compatible upload service for pet photos, certificates, and documents.
6. Add admin panel and moderation workflow for verified reviews.
7. Add tests for routes, forms, and model properties.
