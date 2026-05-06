# Frontend–Backend Contract
## CyphX Real Estate Platform — MVP

## 1. Purpose

This document defines the expected communication contract between the frontend and backend teams.

The goal is to allow both teams to work asynchronously by agreeing on:

- API structure
- expected request and response shapes
- required fields
- entity relationships
- scope boundaries

This contract focuses only on the MVP scope.

---

## 2. Product Scope Reminder

The platform has two main parts:

1. Public website for buyers
2. Private internal dashboard for the seller/admin

The public side allows buyers to browse properties and contact the seller through WhatsApp.

The internal side allows the seller to manage properties, leads, opportunities, notes, and dashboard data.

There are no buyer accounts in the MVP.

---

## 3. General API Rules

### Base API Prefix

```txt
/api/
```

### Response Format

For single objects:

```json
{
  "id": 1,
  "created_at": "2026-05-04T12:00:00Z",
  "updated_at": "2026-05-04T12:00:00Z"
}
```

For list endpoints:

```json
{
  "count": 20,
  "next": null,
  "previous": null,
  "results": []
}
```

### Error Format

```json
{
  "detail": "Error message"
}
```

For validation errors:

```json
{
  "field_name": ["This field is required."]
}
```

### Authentication

Only private/admin endpoints require authentication.

Public property endpoints do not require authentication.

Private endpoints should require an access token.

```http
Authorization: Bearer <access_token>
```

---

# 4. Public API

These endpoints are used by the public website.

No authentication required.

---

## 4.1 List Public Properties

### Endpoint

```http
GET /api/public/properties/
```

### Purpose

Returns publicly visible properties, mainly available properties.

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| search | string | no | Search by title, location, or description |
| city | string | no | Filter by city/location |
| type | string | no | Filter by property type |
| min_price | number | no | Minimum price |
| max_price | number | no | Maximum price |
| status | string | no | Filter by status if allowed publicly |
| ordering | string | no | Example: price, -price, created_at, -created_at |

### Response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title_fr": "Appartement moderne à Casablanca",
      "title_ar": "شقة عصرية بالدار البيضاء",
      "type": "apartment",
      "price": 950000,
      "currency": "MAD",
      "location_fr": "Casablanca",
      "location_ar": "الدار البيضاء",
      "surface": 86,
      "rooms": 3,
      "status": "available",
      "primary_image": "https://example.com/media/properties/image1.jpg"
    }
  ]
}
```

---

## 4.2 Public Property Details

### Endpoint

```http
GET /api/public/properties/{id}/
```

### Purpose

Returns full details of one property for the public detail page.

### Response

```json
{
  "id": 1,
  "title_fr": "Appartement moderne à Casablanca",
  "title_ar": "شقة عصرية بالدار البيضاء",
  "type": "apartment",
  "price": 950000,
  "currency": "MAD",
  "location_fr": "Casablanca",
  "location_ar": "الدار البيضاء",
  "address_fr": "Maarif, Casablanca",
  "address_ar": "المعاريف، الدار البيضاء",
  "surface": 86,
  "rooms": 3,
  "bedrooms": 2,
  "bathrooms": 1,
  "description_fr": "Appartement moderne proche des commodités.",
  "description_ar": "شقة عصرية قريبة من المرافق الأساسية.",
  "features_fr": ["Garage", "Ascenseur", "Balcon"],
  "features_ar": ["مرآب", "مصعد", "شرفة"],
  "status": "available",
  "images": [
    {
      "id": 1,
      "url": "https://example.com/media/properties/image1.jpg",
      "is_primary": true
    }
  ],
  "whatsapp": {
    "phone_number": "+212600000000",
    "contact_message_fr": "Bonjour, je suis intéressé par le bien: Appartement moderne à Casablanca.",
    "visit_message_fr": "Bonjour, je souhaite demander une visite pour le bien: Appartement moderne à Casablanca.",
    "contact_message_ar": "مرحبا، أنا مهتم بهذا العقار: شقة عصرية بالدار البيضاء.",
    "visit_message_ar": "مرحبا، أريد طلب زيارة لهذا العقار: شقة عصرية بالدار البيضاء.",
    "contact_url_fr": "https://wa.me/212600000000?text=...",
    "visit_url_fr": "https://wa.me/212600000000?text=...",
    "contact_url_ar": "https://wa.me/212600000000?text=...",
    "visit_url_ar": "https://wa.me/212600000000?text=..."
  }
}
```

### Frontend Note

The frontend should use the ready-to-use WhatsApp URLs returned by the backend when available.

---

# 5. Authentication API

These endpoints are used by the private dashboard.

---

## 5.1 Login

```http
POST /api/auth/login/
```

### Request

```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

### Response

```json
{
  "access": "access_token_here",
  "refresh": "refresh_token_here",
  "user": {
    "id": 1,
    "full_name": "Admin User",
    "email": "admin@example.com",
    "role": "admin"
  }
}
```

---

## 5.2 Refresh Token

```http
POST /api/auth/refresh/
```

### Request

```json
{
  "refresh": "refresh_token_here"
}
```

### Response

```json
{
  "access": "new_access_token_here"
}
```

---

## 5.3 Current User

```http
GET /api/auth/me/
```

### Response

```json
{
  "id": 1,
  "full_name": "Admin User",
  "email": "admin@example.com",
  "role": "admin"
}
```

---

# 6. Private Properties API

Authentication required.

---

## 6.1 List Properties

```http
GET /api/admin/properties/
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| search | string | no | Search by title/location |
| status | string | no | available, reserved, sold |
| type | string | no | Property type |
| ordering | string | no | price, -price, created_at, -created_at |

### Response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title_fr": "Appartement moderne à Casablanca",
      "title_ar": "شقة عصرية بالدار البيضاء",
      "type": "apartment",
      "price": 950000,
      "currency": "MAD",
      "location_fr": "Casablanca",
      "location_ar": "الدار البيضاء",
      "surface": 86,
      "rooms": 3,
      "status": "available",
      "primary_image": "https://example.com/media/properties/image1.jpg",
      "created_at": "2026-05-04T12:00:00Z",
      "updated_at": "2026-05-04T12:00:00Z"
    }
  ]
}
```

---

## 6.2 Create Property

```http
POST /api/admin/properties/
```

### Request

```json
{
  "title_fr": "Appartement moderne à Casablanca",
  "title_ar": "شقة عصرية بالدار البيضاء",
  "type": "apartment",
  "price": 950000,
  "currency": "MAD",
  "location_fr": "Casablanca",
  "location_ar": "الدار البيضاء",
  "address_fr": "Maarif, Casablanca",
  "address_ar": "المعاريف، الدار البيضاء",
  "surface": 86,
  "rooms": 3,
  "bedrooms": 2,
  "bathrooms": 1,
  "description_fr": "Appartement moderne proche des commodités.",
  "description_ar": "شقة عصرية قريبة من المرافق الأساسية.",
  "features_fr": ["Garage", "Ascenseur", "Balcon"],
  "features_ar": ["مرآب", "مصعد", "شرفة"],
  "status": "available",
  "is_public": true
}
```

### Response

Returns the created property object.

---

## 6.3 Property Details

```http
GET /api/admin/properties/{id}/
```

### Response

```json
{
  "id": 1,
  "title_fr": "Appartement moderne à Casablanca",
  "title_ar": "شقة عصرية بالدار البيضاء",
  "type": "apartment",
  "price": 950000,
  "currency": "MAD",
  "location_fr": "Casablanca",
  "location_ar": "الدار البيضاء",
  "address_fr": "Maarif, Casablanca",
  "address_ar": "المعاريف، الدار البيضاء",
  "surface": 86,
  "rooms": 3,
  "bedrooms": 2,
  "bathrooms": 1,
  "description_fr": "Appartement moderne proche des commodités.",
  "description_ar": "شقة عصرية قريبة من المرافق الأساسية.",
  "features_fr": ["Garage", "Ascenseur", "Balcon"],
  "features_ar": ["مرآب", "مصعد", "شرفة"],
  "status": "available",
  "is_public": true,
  "images": [
    {
      "id": 1,
      "url": "https://example.com/media/properties/image1.jpg",
      "is_primary": true
    }
  ],
  "interested_leads": [
    {
      "id": 3,
      "full_name": "Youssef Amrani",
      "phone": "+212600000000"
    }
  ],
  "created_at": "2026-05-04T12:00:00Z",
  "updated_at": "2026-05-04T12:00:00Z"
}
```

---

## 6.4 Update Property

```http
PATCH /api/admin/properties/{id}/
```

### Request Example

```json
{
  "price": 920000,
  "status": "reserved"
}
```

### Response

Returns the updated property object.

---

## 6.5 Delete or Archive Property

```http
DELETE /api/admin/properties/{id}/
```

### Response

```json
{
  "detail": "Property deleted successfully."
}
```

Recommended implementation: soft delete or archive if possible.

---

## 6.6 Upload Property Image

```http
POST /api/admin/properties/{id}/images/
```

### Request

Multipart form-data:

```txt
image: file
is_primary: true
```

### Response

```json
{
  "id": 1,
  "url": "https://example.com/media/properties/image1.jpg",
  "is_primary": true
}
```

---

## 6.7 Delete Property Image

```http
DELETE /api/admin/property-images/{id}/
```

### Response

```json
{
  "detail": "Image deleted successfully."
}
```

---

# 7. Leads API

Authentication required.

A lead is an internal record only. It is not a user account.

---

## 7.1 List Leads

```http
GET /api/admin/leads/
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| search | string | no | Search by name, phone, email |
| source | string | no | whatsapp, referral, direct, other |
| ordering | string | no | created_at, -created_at |

### Response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "full_name": "Youssef Amrani",
      "phone": "+212600000000",
      "email": "youssef@example.com",
      "budget_min": 700000,
      "budget_max": 1000000,
      "source": "whatsapp",
      "created_at": "2026-05-04T12:00:00Z"
    }
  ]
}
```

---

## 7.2 Create Lead

```http
POST /api/admin/leads/
```

### Request

```json
{
  "full_name": "Youssef Amrani",
  "phone": "+212600000000",
  "email": "youssef@example.com",
  "budget_min": 700000,
  "budget_max": 1000000,
  "preferences": "Interested in Casablanca apartments with garage.",
  "source": "whatsapp"
}
```

### Response

Returns the created lead object.

---

## 7.3 Lead Details

```http
GET /api/admin/leads/{id}/
```

### Response

```json
{
  "id": 3,
  "full_name": "Youssef Amrani",
  "phone": "+212600000000",
  "email": "youssef@example.com",
  "budget_min": 700000,
  "budget_max": 1000000,
  "preferences": "Interested in Casablanca apartments with garage.",
  "source": "whatsapp",
  "interested_properties": [
    {
      "id": 1,
      "title_fr": "Appartement moderne à Casablanca",
      "title_ar": "شقة عصرية بالدار البيضاء",
      "price": 950000,
      "status": "available"
    }
  ],
  "opportunities": [
    {
      "id": 5,
      "stage": "interested",
      "status": "open",
      "property": {
        "id": 1,
        "title_fr": "Appartement moderne à Casablanca",
        "title_ar": "شقة عصرية بالدار البيضاء"
      }
    }
  ],
  "recent_interactions": [
    {
      "id": 10,
      "type": "call",
      "content": "Client asked about payment options.",
      "interaction_date": "2026-05-04T12:00:00Z"
    }
  ],
  "created_at": "2026-05-04T12:00:00Z",
  "updated_at": "2026-05-04T12:00:00Z"
}
```

---

## 7.4 Update Lead

```http
PATCH /api/admin/leads/{id}/
```

### Request Example

```json
{
  "budget_max": 1100000,
  "preferences": "Prefers higher floor."
}
```

### Response

Returns the updated lead object.

---

## 7.5 Delete Lead

```http
DELETE /api/admin/leads/{id}/
```

### Response

```json
{
  "detail": "Lead deleted successfully."
}
```

---

# 8. Lead–Property Interest API

Authentication required.

---

## 8.1 Create Interest

```http
POST /api/admin/lead-property-interests/
```

### Request

```json
{
  "lead_id": 3,
  "property_id": 1,
  "interest_level": "high"
}
```

### Response

```json
{
  "id": 1,
  "lead": {
    "id": 3,
    "full_name": "Youssef Amrani"
  },
  "property": {
    "id": 1,
    "title_fr": "Appartement moderne à Casablanca",
    "title_ar": "شقة عصرية بالدار البيضاء"
  },
  "interest_level": "high",
  "created_at": "2026-05-04T12:00:00Z"
}
```

---

## 8.2 Delete Interest

```http
DELETE /api/admin/lead-property-interests/{id}/
```

### Response

```json
{
  "detail": "Interest deleted successfully."
}
```

---

# 9. Pipeline Stages API

Authentication required.

---

## 9.1 List Pipeline Stages

```http
GET /api/admin/pipeline-stages/
```

### Response

```json
[
  { "id": 1, "name": "Nouveau lead", "slug": "new_lead", "order": 1 },
  { "id": 2, "name": "Contacté", "slug": "contacted", "order": 2 },
  { "id": 3, "name": "Intéressé", "slug": "interested", "order": 3 },
  { "id": 4, "name": "Visite planifiée", "slug": "visit_planned", "order": 4 },
  { "id": 5, "name": "Négociation", "slug": "negotiation", "order": 5 },
  { "id": 6, "name": "Réservé", "slug": "reserved", "order": 6 },
  { "id": 7, "name": "Vendu", "slug": "sold", "order": 7 },
  { "id": 8, "name": "Perdu", "slug": "lost", "order": 8 }
]
```

---

# 10. Opportunities API

Authentication required.

An opportunity represents a sales process with a lead.

---

## 10.1 List Opportunities

```http
GET /api/admin/opportunities/
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| stage | string | no | Stage slug |
| status | string | no | open, won, lost |
| lead | number | no | Lead id |
| property | number | no | Property id |

### Response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "lead": {
        "id": 3,
        "full_name": "Youssef Amrani",
        "phone": "+212600000000"
      },
      "property": {
        "id": 1,
        "title_fr": "Appartement moderne à Casablanca",
        "title_ar": "شقة عصرية بالدار البيضاء",
        "price": 950000
      },
      "stage": {
        "id": 3,
        "name": "Intéressé",
        "slug": "interested"
      },
      "status": "open",
      "notes": "Client interested after WhatsApp discussion.",
      "created_at": "2026-05-04T12:00:00Z",
      "updated_at": "2026-05-04T12:00:00Z"
    }
  ]
}
```

---

## 10.2 Create Opportunity

```http
POST /api/admin/opportunities/
```

### Request

```json
{
  "lead_id": 3,
  "property_id": 1,
  "stage_id": 3,
  "notes": "Client interested after WhatsApp discussion."
}
```

### Response

Returns the created opportunity object.

---

## 10.3 Opportunity Details

```http
GET /api/admin/opportunities/{id}/
```

### Response

```json
{
  "id": 5,
  "lead": {
    "id": 3,
    "full_name": "Youssef Amrani",
    "phone": "+212600000000",
    "email": "youssef@example.com"
  },
  "property": {
    "id": 1,
    "title_fr": "Appartement moderne à Casablanca",
    "title_ar": "شقة عصرية بالدار البيضاء",
    "price": 950000,
    "status": "available"
  },
  "stage": {
    "id": 3,
    "name": "Intéressé",
    "slug": "interested"
  },
  "status": "open",
  "notes": "Client interested after WhatsApp discussion.",
  "interactions": [
    {
      "id": 10,
      "type": "call",
      "content": "Client asked about payment options.",
      "interaction_date": "2026-05-04T12:00:00Z"
    }
  ],
  "created_at": "2026-05-04T12:00:00Z",
  "updated_at": "2026-05-04T12:00:00Z"
}
```

---

## 10.4 Update Opportunity

```http
PATCH /api/admin/opportunities/{id}/
```

### Request Example

```json
{
  "notes": "Client wants to visit this week."
}
```

### Response

Returns the updated opportunity object.

---

## 10.5 Move Opportunity Stage

```http
PATCH /api/admin/opportunities/{id}/move-stage/
```

### Request

```json
{
  "stage_id": 5
}
```

### Response

```json
{
  "id": 5,
  "stage": {
    "id": 5,
    "name": "Négociation",
    "slug": "negotiation"
  },
  "status": "open",
  "updated_at": "2026-05-04T12:00:00Z"
}
```

### Business Rules

- If stage becomes `sold`, opportunity status becomes `won`.
- If stage becomes `lost`, opportunity status becomes `lost`.
- If stage becomes `reserved`, related property may become `reserved`.
- If stage becomes `sold`, related property may become `sold`.

---

## 10.6 Delete Opportunity

```http
DELETE /api/admin/opportunities/{id}/
```

### Response

```json
{
  "detail": "Opportunity deleted successfully."
}
```

---

# 11. Interactions API

Authentication required.

---

## 11.1 List Interactions

```http
GET /api/admin/interactions/
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| lead | number | no | Lead id |
| opportunity | number | no | Opportunity id |
| property | number | no | Property id |
| type | string | no | call, whatsapp, visit, note |

### Response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 10,
      "type": "call",
      "title": "First call",
      "content": "Client asked about payment options.",
      "lead": {
        "id": 3,
        "full_name": "Youssef Amrani"
      },
      "property": {
        "id": 1,
        "title_fr": "Appartement moderne à Casablanca",
        "title_ar": "شقة عصرية بالدار البيضاء"
      },
      "opportunity": {
        "id": 5
      },
      "interaction_date": "2026-05-04T12:00:00Z",
      "created_at": "2026-05-04T12:00:00Z"
    }
  ]
}
```

---

## 11.2 Create Interaction

```http
POST /api/admin/interactions/
```

### Request

```json
{
  "type": "call",
  "title": "First call",
  "content": "Client asked about payment options.",
  "lead_id": 3,
  "property_id": 1,
  "opportunity_id": 5,
  "interaction_date": "2026-05-04T12:00:00Z"
}
```

### Response

Returns the created interaction object.

---

## 11.3 Update Interaction

```http
PATCH /api/admin/interactions/{id}/
```

### Request Example

```json
{
  "content": "Client confirmed interest and wants a visit."
}
```

### Response

Returns the updated interaction object.

---

## 11.4 Delete Interaction

```http
DELETE /api/admin/interactions/{id}/
```

### Response

```json
{
  "detail": "Interaction deleted successfully."
}
```

---

# 12. Dashboard API

Authentication required.

---

## 12.1 Dashboard Overview

```http
GET /api/admin/dashboard/overview/
```

### Response

```json
{
  "properties": {
    "total": 30,
    "available": 20,
    "reserved": 5,
    "sold": 5
  },
  "leads": {
    "total": 45,
    "active": 32
  },
  "opportunities": {
    "total": 35,
    "open": 25,
    "won": 5,
    "lost": 5
  }
}
```

---

## 12.2 Pipeline Summary

```http
GET /api/admin/dashboard/pipeline-summary/
```

### Response

```json
[
  {
    "stage": {
      "id": 1,
      "name": "Nouveau lead",
      "slug": "new_lead"
    },
    "count": 8
  },
  {
    "stage": {
      "id": 2,
      "name": "Contacté",
      "slug": "contacted"
    },
    "count": 6
  }
]
```

---

## 12.3 Recent Activities

Optional for MVP if interactions are already listed elsewhere.

```http
GET /api/admin/dashboard/recent-activities/
```

### Response

```json
[
  {
    "id": 10,
    "type": "interaction",
    "title": "First call",
    "description": "Client asked about payment options.",
    "created_at": "2026-05-04T12:00:00Z"
  }
]
```

---

# 13. Language Support

The MVP must support:

- French
- Arabic

Spanish is planned for a later version.

## Backend Responsibility

For fast implementation, the backend should expose separate multilingual fields:

```json
{
  "title_fr": "Appartement moderne à Casablanca",
  "title_ar": "شقة عصرية بالدار البيضاء",
  "description_fr": "Appartement moderne proche des commodités.",
  "description_ar": "شقة عصرية قريبة من المرافق الأساسية."
}
```

The backend should not implement Spanish fields in MVP unless explicitly approved.

## Frontend Responsibility

The frontend chooses which field to display depending on the selected language.

---

# 14. Static Configuration API

Optional but useful.

---

## 14.1 Public App Settings

```http
GET /api/public/settings/
```

### Response

```json
{
  "seller_name": "Nom du vendeur",
  "whatsapp_phone": "+212600000000",
  "default_language": "fr",
  "supported_languages": ["fr", "ar"],
  "future_languages": ["es"]
}
```

---

# 15. Enum Values

Backend and frontend must use the same values.

## Property Status

```txt
available
reserved
sold
```

## Property Types

```txt
apartment
villa
house
land
office
store
other
```

## Lead Sources

```txt
whatsapp
referral
direct
facebook
instagram
website
other
```

## Opportunity Status

```txt
open
won
lost
```

## Interaction Types

```txt
call
whatsapp
visit
note
other
```

## Pipeline Stage Slugs

```txt
new_lead
contacted
interested
visit_planned
negotiation
reserved
sold
lost
```

---

# 16. MVP Boundaries

The backend should not implement the following in this iteration:

- buyer accounts
- buyer login/signup
- online visit booking system
- calendar slots
- online payment
- contract generation
- rental management
- advanced automation
- AI matching
- complex multi-agency features
- Spanish language support in MVP

---

# 17. Backend Delivery Checklist

The backend team should deliver:

- authentication endpoints
- public property listing endpoint
- public property details endpoint
- public settings endpoint if used
- private property CRUD
- image upload/delete
- private lead CRUD
- lead-property interest endpoints
- pipeline stages endpoint
- opportunity CRUD
- opportunity stage movement
- interaction CRUD
- dashboard overview
- consistent validation errors
- API documentation

---

# 18. Frontend Mocking Guide

Frontend can start before backend is finished by mocking the response shapes defined in this document.

Recommended frontend mock files:

```txt
mockProperties.ts
mockLeads.ts
mockOpportunities.ts
mockDashboard.ts
mockSettings.ts
```

The frontend should build components using the same field names defined here to reduce integration issues later.

---

# 19. Integration Rules

Before integration, both teams should verify:

- endpoint paths match this contract
- field names match this contract
- enum values match this contract
- response shapes match this contract
- auth flow works with access token
- public endpoints work without login
- private endpoints reject unauthenticated requests

---

# 20. Final Note

This contract is intentionally limited to the MVP.

Any feature not defined here should be considered out of scope unless explicitly approved.
