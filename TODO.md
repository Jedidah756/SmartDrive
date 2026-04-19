# Fix Render 500 Error After Login
Status: Steps 1-4 complete - Ready for deploy/test

## Step 1: Verify seed_demo creates necessary data ✓
- [x] Read seed_demo.py 
- [x] Run seed_demo locally (executed)
- [x] Confirmed creates Users/Vehicles/Routes/Schedules

## Step 2: Update render.yaml to seed data on build ✓
- [x] Added `&& python manage.py seed_demo` to buildCommand
- [ ] Redeploy: git add . && git commit -m "add seed_demo to render build" && git push (user action)

## Step 3: Make DashboardRedirectView robust ✓
- [x] Added try/except around ensure_daily_trips() with logging in accounts/views.py
- Fallback to role redirect works

## Step 4: Add logging to gunicorn ✓
- [x] Added --log-level debug to startCommand in render.yaml

## Step 5: Test
- Local: DEBUG=False, empty SQLite, migrate, seed, login test
- Render: redeploy, live login test, check logs

## Step 6: Handle empty dashboards
- Update dashboard views to handle zero data gracefully

## Step 2: Update render.yaml to seed data on build
- Edit render.yaml buildCommand to include `&& cd campus_transport && python manage.py seed_demo`
- Redeploy on Render

## Step 3: Make DashboardRedirectView robust
- Edit accounts/views.py: wrap ensure_daily_trips() in try/except, log error if fails
- Fallback to role redirect without trips

## Step 4: Add logging to gunicorn
- Update render.yaml startCommand: gunicorn ... --log-level debug

## Step 5: Test
- Local: DEBUG=False, empty SQLite, migrate, seed, login test
- Render: redeploy, live login test, check logs

## Step 6: Handle empty dashboards
- Update dashboard views to handle zero data gracefully

