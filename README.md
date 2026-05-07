# Web-Based Rental Brokerage Automation System

Localized rental brokerage system for Kampala metropolitan areas. Prices are shown in UGX.

## Features
- Register/login/logout
- Tenant and Landlord roles
- Landlord property posting
- Area dropdowns within scope
- UGX rental prices
- Image and video uploads
- Admin approval before public display
- Search/filter by area and UGX price range
- Tenant inquiries to landlords

## Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000
