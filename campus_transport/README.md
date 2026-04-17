# Campus Transport Management System

Campus Transport is a Django-based university transport platform for students, drivers, transport administrators, and super administrators. It supports route management, trip tracking, simulated live bus positions, student feedback, reports, and exportable analytics.

## Features

- Role-based access control for students, drivers, transport admins, and super admins
- Route, vehicle, schedule, trip, booking, feedback, incident, and report management
- Simulated live bus tracking with polling-friendly JSON endpoints
- Dashboard cards, charts, toast alerts, and responsive dark university styling
- PDF and CSV report export scaffolding
- Seed command with demo data across major tables

## Tech Stack

- Django 5
- SQLite for local development, MySQL optional for deployment/demo parity
- HTML, CSS, and vanilla JavaScript
- Google Maps JavaScript API
- Chart.js
- WeasyPrint / ReportLab

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`.
4. For quick local setup, leave `DB_ENGINE=sqlite`.
5. Run migrations:

```bash
python manage.py migrate
```

6. Seed demo data:

```bash
python manage.py seed_demo
```

7. Start the development server:

```bash
python manage.py runserver
```

## Demo Credentials

- Super Admin: `superadmin@demo.local` / `DemoPass123!`
- Transport Admin: `admin@demo.local` / `DemoPass123!`
- Driver: `driver1@demo.local` / `DemoPass123!`
- Student: `student1@demo.local` / `DemoPass123!`

## Google Maps Setup

1. Create a Google Maps JavaScript API key in Google Cloud Console.
2. Enable the Maps JavaScript API.
3. Add the key to `GOOGLE_MAPS_API_KEY` in `.env`.
4. Open the dashboards with live map panels to see markers and route polylines.

## Notes

- The project uses session authentication and Django's built-in admin as the fallback super admin interface.
- JSON endpoints under `/trips/api/` are designed for 15-second frontend polling.
- To use MySQL instead, set `DB_ENGINE=mysql` in `.env`, make sure the MySQL service is running, and create a `campus_transport` database first.
