# TODO (progress)

- [x] Inspect repo structure and core accounts/dashboard/seed logic
- [ ] Fix `ImportError` preventing `python manage.py check` from running
  - [ ] Add missing `DriverRegistrationForm` to `apps/accounts/forms.py`
  - [ ] Add driver registration form fields + role assignment
  - [ ] Re-run `python manage.py check`
- [ ] If checks pass, run migrations and (optionally) seed_demo
  - [ ] `python manage.py migrate`
  - [ ] `python manage.py seed_demo`


