# CyphX Real Estate Platform — PERSON_A Implementation Plan

---

## 1. Document Summary

### Cahier de Charge (CC)

The MVP is a two-sided real estate platform:

| Side | Who | Core need |
|---|---|---|
| **Public** | Buyers | Browse properties, contact seller via WhatsApp |
| **Internal** | Seller/Admin | Manage properties, leads, pipeline, notes, dashboard |

**Key constraints:**
- No buyer accounts, no reservations, no payments, no AI — MVP only
- Bilingual: French + Arabic (Spanish is post-MVP)
- Target users: independent agents, brokers, small developers

---

### Backend–Backend Contract

Two persons split the backend cleanly:

| Person | Scope |
|---|---|
| **PERSON_A (me)** | Project setup, auth, users, properties, images, public API, public settings |
| **PERSON_B** | Leads, CRM, pipeline, opportunities, interactions, dashboard |

**PERSON_A owns these Django apps:** `accounts/`, `properties/`, `core/`

**PERSON_A must NOT touch:** leads, opportunities, interactions, pipeline, dashboard CRM stats.

**PERSON_B depends on PERSON_A's `Property` model** — must be kept stable once CRM work begins.

---

### Frontend–Backend Contract

| Category | Key rules |
|---|---|
| **URL namespacing** | Public `/api/public/`, Admin `/api/admin/`, Auth `/api/auth/` |
| **List responses** | Paginated: `{count, next, previous, results:[]}` |
| **Single objects** | Flat JSON with `id`, `created_at`, `updated_at` |
| **Errors** | `{"detail": "..."}` or `{"field": ["msg"]}` |
| **Auth** | JWT Bearer token — public endpoints open, admin require token |
| **Multilingual** | Separate `_fr` / `_ar` fields, no translation layer |
| **WhatsApp** | Pre-built URLs returned by backend in public property detail |

---

## 2. PERSON_A Endpoint Checklist

```
Auth
  POST /api/auth/login/
  POST /api/auth/refresh/
  GET  /api/auth/me/

Public
  GET  /api/public/settings/
  GET  /api/public/properties/        (with filters)
  GET  /api/public/properties/{id}/   (with WhatsApp URLs)

Admin Properties
  GET    /api/admin/properties/
  POST   /api/admin/properties/
  GET    /api/admin/properties/{id}/
  PATCH  /api/admin/properties/{id}/
  DELETE /api/admin/properties/{id}/
  POST   /api/admin/properties/{id}/images/
  DELETE /api/admin/property-images/{id}/
```

---

## 3. Proposed Project Structure

```
neroli-backend/
├── config/                    # Django project root
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  # PERSON_A — Auth & Users
│   ├── models.py              # CustomUser
│   ├── serializers.py
│   ├── views.py               # login, refresh, me
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── properties/                # PERSON_A — Properties & Images
│   ├── models.py              # Property, PropertyImage
│   ├── serializers.py         # Public + Admin serializers
│   ├── views.py               # Public + Admin viewsets
│   ├── filters.py             # Search, type, price, status
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
│
├── core/                      # PERSON_A — Shared config & utilities
│   ├── models.py              # PublicSettings
│   ├── serializers.py
│   ├── views.py               # GET /api/public/settings/
│   ├── urls.py
│   └── migrations/
│
├── media/                     # Uploaded property images
├── requirements.txt
├── .env.example
├── manage.py
└── README.md
```

> **Note for PERSON_B:** Apps `leads/`, `crm/`, `interactions/`, `dashboard/` are reserved and will be added later.

---

## 4. Key Model Decisions

### CustomUser
- Extends `AbstractBaseUser` + `PermissionsMixin`
- Login via **email** (`USERNAME_FIELD = 'email'`)
- `role` field: `admin` (+ `agent` optional)
- Custom `UserManager` required

### Property
- All bilingual fields stored as `_fr` / `_ar` variants
- `features_fr` / `features_ar` stored as `JSONField` (list of strings)
- `is_public` flag controls public visibility
- `status` choices: `available`, `reserved`, `sold`
- `type` choices: `apartment`, `villa`, `house`, `land`, `office`, `store`, `other`
- `currency` default: `MAD`
- `rooms`, `bedrooms`, `bathrooms`, `surface` are nullable

### PropertyImage
- FK to `Property`, `on_delete=CASCADE`
- `image = ImageField` → stored under `media/properties/`
- `is_primary = BooleanField`
- `url` computed in serializer from request context

### PublicSettings
- Singleton model (one row)
- Fields: `seller_name`, `whatsapp_phone`, `default_language`, `supported_languages` (JSONField)

---

## 5. WhatsApp URL Generation

```python
# lives in properties/serializers.py
from urllib.parse import quote

def get_whatsapp_block(property_obj, phone):
    base = f"https://wa.me/{phone.replace('+', '')}"
    msg_contact_fr = f"Bonjour, je suis interess?? par le bien: {property_obj.title_fr}."
    msg_visit_fr   = f"Bonjour, je souhaite demander une visite pour le bien: {property_obj.title_fr}."
    msg_contact_ar = f"????????, ?????? ???????? ???????? ????????????: {property_obj.title_ar}."
    msg_visit_ar   = f"????????, ???????? ?????? ???????? ???????? ????????????: {property_obj.title_ar}."
    return {
        "phone_number": phone,
        "contact_message_fr": msg_contact_fr,
        "visit_message_fr": msg_visit_fr,
        "contact_message_ar": msg_contact_ar,
        "visit_message_ar": msg_visit_ar,
        "contact_url_fr": f"{base}?text={quote(msg_contact_fr)}",
        "visit_url_fr":   f"{base}?text={quote(msg_visit_fr)}",
        "contact_url_ar": f"{base}?text={quote(msg_contact_ar)}",
        "visit_url_ar":   f"{base}?text={quote(msg_visit_ar)}",
    }
```

---

## 6. `interested_leads` in Admin Property Detail

Backend-Backend Contract §7.3 offers two options.
**MVP choice: Option B** — PERSON_A returns property details without `interested_leads`.
Frontend fetches interested leads through PERSON_B's endpoints.
This will be coordinated with PERSON_B post-integration.

---

## 7. Implementation Phases

### Phase 1 — Project Setup
- [ ] Django project in `config/`
- [ ] Install + freeze dependencies
- [ ] Split settings: `base.py`, `development.py`, `production.py`
- [ ] Configure DRF, JWT, CORS, media
- [ ] Create `.env.example`
- [ ] Wire `config/urls.py`

### Phase 2 — Auth (accounts app)
- [ ] `CustomUser` model + `UserManager`
- [ ] JWT login view (returns `{access, refresh, user}`)
- [ ] Refresh view
- [ ] `/api/auth/me/` (IsAuthenticated)
- [ ] `UserSerializer`
- [ ] Django admin registration

### Phase 3 — Properties (properties app)
- [ ] `Property` + `PropertyImage` models
- [ ] Migrations
- [ ] All serializers (Public list, Public detail, Admin list, Admin detail, Create/Update, Image)
- [ ] `PropertyFilter` (search, city, type, min_price, max_price, status, ordering)
- [ ] Public viewset (read-only, open, `is_public=True`)
- [ ] Admin viewset (full CRUD, IsAuthenticated)
- [ ] Image upload + delete actions
- [ ] URL registration

### Phase 4 — Core / Public Settings (core app)
- [ ] `PublicSettings` model
- [ ] Serializer
- [ ] `GET /api/public/settings/` view
- [ ] Django admin registration

### Phase 5 — Polish & Handoff
- [ ] Verify all URLs match contract exactly
- [ ] Ensure 401 on admin endpoints without token
- [ ] Ensure 200 on public endpoints without token
- [ ] Default pagination: `PageNumberPagination`, page_size=20
- [ ] Manual test all endpoints
- [ ] Write `README.md`
- [ ] Note for PERSON_B: Property model fields, stable FK reference

---

## 8. Dependencies (requirements.txt)

```
Django>=4.2,<5.0
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
django-filter>=23.0
django-cors-headers>=4.3
Pillow>=10.0
python-decouple>=3.8
dj-database-url>=2.1
```

---

## 9. Open Questions

| # | Question | Recommended default |
|---|---|---|
| 1 | Database for dev? | SQLite (dev), Postgres-ready via `dj-database-url` |
| 2 | Media storage? | Local for MVP, structure ready for S3 |
| 3 | `interested_leads` in admin property detail? | Option B (skip, coordinate with PERSON_B) |
| 4 | Soft-delete or hard-delete for properties? | Hard delete for MVP simplicity |
| 5 | `PublicSettings`: model or settings constant? | Model-based (admin-editable) |

---

> Confirm the open questions above (or accept recommended defaults) to start coding Phase 1.
