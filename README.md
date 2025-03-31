# Django Project Setup Guide

## 1. Create a Python Virtual Environment
```sh
python -m venv .venv
```

## 2. Activate the Virtual Environment
- **Windows**:
  ```sh
  .venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```sh
  source .venv/bin/activate
  ```

## 3. Install Django
```sh
pip install django
```

## 4. Create Django Project `payment_gateway_provider`
```sh
django-admin startproject payment_gateway_provider
```

## 5. Navigate to the Project Directory
```sh
cd payment_gateway_provider
```

## 6. Create Django Apps
```sh
python manage.py startapp payments
python manage.py startapp users
python manage.py startapp transactions
```

## 7. Configure `settings.py`
- Add the created apps to `INSTALLED_APPS`:
  ```python
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'payments',
      'users',
      'transactions',
  ]
  ```
- Configure Database, Middleware, and Static files as needed.

## 8. Create Migrations
```sh
python manage.py makemigrations
python manage.py migrate
```

## 9. Run the Development Server
```sh
python manage.py runserver
```

## 10. Create a Superuser (for Admin Panel)
```sh
python manage.py createsuperuser
```

## 11. Run Tests
```sh
python manage.py test
```

## 12. Deactivate the Virtual Environment (if needed)
```sh
deactivate
