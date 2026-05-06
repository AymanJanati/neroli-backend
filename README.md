# CyphX Real Estate Platform — Backend MVP

This is the backend for the CyphX Real Estate Platform (MVP).
It is a Django REST Framework application.

## Prerequisites

- Python 3.10+
- virtualenv or similar

## Initial Setup

1. **Clone the repository and set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows PowerShell
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Copy `.env.example` to `.env` and fill in the values.
   ```bash
   cp .env.example .env
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser** (Admin account)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## Note for PERSON_B (CRM & Sales Team)

1. The `Property` model is owned by **PERSON_A** and lives in the `properties` app. Use it as a `ForeignKey` reference for leads and opportunities. The structure matches the Backend-Backend contract exactly.
2. The property detail for admin (`AdminPropertyDetailSerializer`) does **not** include `interested_leads` to respect Option B of the contract. You'll query leads by property ID using your CRM endpoints.
3. Your apps (`leads`, `crm`, `interactions`, `dashboard`) should be added to `LOCAL_APPS` in `config/settings/base.py` once created.
4. Mount your admin URLs into `config/urls.py` under the `/api/admin/` prefix.

## Endpoints Implemented (Phase 1)

- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET  /api/auth/me/`
- `GET  /api/public/settings/`
- `GET  /api/public/properties/`
- `GET  /api/public/properties/<id>/`
- `GET, POST /api/admin/properties/`
- `GET, PATCH, DELETE /api/admin/properties/<id>/`
- `POST /api/admin/properties/<id>/images/`
- `DELETE /api/admin/property-images/<id>/`
