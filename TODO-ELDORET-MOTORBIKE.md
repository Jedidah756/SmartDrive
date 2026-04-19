# Update to Eldoret/Nandi + Add Motorbikes
Status: Step 1 ✓

## Step 1: Fix logger in views.py ✓
- [x] Moved import logging top, logger module-level, used in except

## Step 2: Update seed_demo.py ✓
- [x] Replaced routes with 4 bus + 1 motorbike Eldoret/Nandi routes (approx coords)
- [x] Added 3 motorbike vehicles (Bajaj/TVS/Piaggio, cap 3-4)
- Schedules auto-use new vehicles/drivers

## Step 3: Test seed & deploy
- Run seed_demo locally, check Routes/Vehicles
- Git push → Render rebuild

## Step 4: Verify maps/dashboards
- Login test on Render, check new locations on maps

