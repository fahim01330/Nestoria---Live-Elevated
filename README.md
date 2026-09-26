# Property Rental & Management System

Django project implementing the supplied Module 11 assignment: authentication, Owner/Tenant roles, property CRUD, search/filtering, rental requests, dashboards, reviews/ratings, admin, middleware, permissions and image upload.

## Setup
`python -m venv venv`

Windows: `venv\Scripts\activate`

`pip install -r requirements.txt`
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py createsuperuser`
`python manage.py runserver`

Website: http://127.0.0.1:8000/
Admin: http://127.0.0.1:8000/admin/

Do not commit .env, passwords, API keys or production secret keys.
