# Backend–Backend Contract

## CyphX Real Estate Platform — MVP

> This contract is designed for AI coding / vibe coding.  
> Each backend developer must keep their assigned side clear and avoid modifying the other side unless explicitly coordinated.

---

# 0. Assignment Header

## Project

CyphX Real Estate Platform — Backend MVP

AI USAGE:
Before using this contract with an AI coding assistant, the developer must state their role manually:

"I am PERSON_A. Follow only PERSON_A responsibilities."

or

"I am PERSON_B. Follow only PERSON_B responsibilities."

---

# 1. Purpose

This contract defines how two backend developers will split the backend implementation.

The goal is to allow both people to work in parallel without breaking each other’s work.

The backend must respect the Frontend–Backend Contract for:

- endpoint paths
- response shapes
- enum values
- authentication behavior
- MVP boundaries

---

# 2. Global Backend Rules

Both people must respect these rules.

## 2.1 Do Not Break the API Contract

All endpoints, field names, response structures, and enum values must follow the agreed frontend–backend contract.

## 2.2 MVP Only

Do not implement:

- buyer accounts
- buyer login/signup
- online booking calendar
- payment
- contract generation
- rental management
- AI matching
- Spanish fields
- complex multi-agency logic

## 2.3 Language Support

The MVP supports:

- French
- Arabic

Use separate fields where needed:

```txt
title_fr
title_ar
description_fr
description_ar
location_fr
location_ar
address_fr
address_ar
features_fr
features_ar
```

Spanish is planned later and should not be implemented now.

## 2.4 Authentication

Only private/admin endpoints require authentication.

Public endpoints must work without login.

## 2.5 Public vs Admin API

Public endpoints use:

```txt
/api/public/
```

Admin/private endpoints use:

```txt
/api/admin/
```

Auth endpoints use:

```txt
/api/auth/
```

---

# 3. Work Split Summary

## PERSON_A — Core Platform & Property Side

PERSON_A owns:

- project setup
- global settings
- authentication
- users/admin access
- public settings
- properties
- property images
- public property catalog
- API documentation base
- shared enums/constants related to properties

## PERSON_B — CRM & Sales Side

PERSON_B owns:

- leads
- lead-property interests
- pipeline stages
- opportunities
- interactions/notes
- dashboard
- CRM business rules
- shared enums/constants related to CRM

---

# 4. Shared Foundation

The following files/modules are shared and must be coordinated.

## Shared Areas

```txt
config/
common/
requirements.txt
.env.example
README.md
```

## Rule

If one person changes shared files, they must clearly document the change in the pull request or commit message.

Avoid large unrelated edits in shared files.

---

# 5. PERSON_A Scope

## 5.1 Main Responsibility

PERSON_A builds the foundation and the property/public side of the backend.

This side makes the platform usable for:

- public property browsing
- admin property management
- property image management
- authentication

---

## 5.2 Apps Owned by PERSON_A

Recommended apps:

```txt
accounts/
properties/
core/
```

Optional:

```txt
public_api/
```

---

## 5.3 Models Owned by PERSON_A

### User

Fields:

```txt
id
full_name
email
password
role
is_active
created_at
updated_at
```

Roles for MVP:

```txt
admin
```

Optional:

```txt
agent
```

### Property

Fields:

```txt
id
title_fr
title_ar
type
price
currency
location_fr
location_ar
address_fr
address_ar
surface
rooms
bedrooms
bathrooms
description_fr
description_ar
features_fr
features_ar
status
is_public
created_at
updated_at
```

Property status values:

```txt
available
reserved
sold
```

Property type values:

```txt
apartment
villa
house
land
office
store
other
```

### PropertyImage

Fields:

```txt
id
property
image
is_primary
created_at
```

### PublicSettings

Can be model-based or settings-based.

Expected public output:

```txt
seller_name
whatsapp_phone
default_language
supported_languages
future_languages
```

---

## 5.4 Endpoints Owned by PERSON_A

### Auth

```http
POST /api/auth/login/
POST /api/auth/refresh/
GET /api/auth/me/
```

### Public Settings

```http
GET /api/public/settings/
```

### Public Properties

```http
GET /api/public/properties/
GET /api/public/properties/{id}/
```

### Admin Properties

```http
GET /api/admin/properties/
POST /api/admin/properties/
GET /api/admin/properties/{id}/
PATCH /api/admin/properties/{id}/
DELETE /api/admin/properties/{id}/
```

### Property Images

```http
POST /api/admin/properties/{id}/images/
DELETE /api/admin/property-images/{id}/
```

---

## 5.5 PERSON_A Must Provide

PERSON_A must provide working serializers for:

```txt
PublicPropertyListSerializer
PublicPropertyDetailSerializer
AdminPropertyListSerializer
AdminPropertyDetailSerializer
PropertyCreateUpdateSerializer
PropertyImageSerializer
UserSerializer
LoginResponseSerializer if needed
```

PERSON_A must provide filters for:

```txt
search
city/location
type
min_price
max_price
status
ordering
```

PERSON_A must provide WhatsApp URLs in public property details:

```txt
contact_url_fr
visit_url_fr
contact_url_ar
visit_url_ar
```

---

## 5.6 PERSON_A Must Not Implement

PERSON_A should not implement:

- leads
- opportunities
- interactions
- pipeline logic
- dashboard CRM stats

PERSON_A may expose property-related helper methods needed by PERSON_B, but should not own CRM behavior.

---

# 6. PERSON_B Scope

## 6.1 Main Responsibility

PERSON_B builds the internal CRM and sales tracking side.

This side makes the platform usable for:

- managing leads
- linking leads to properties
- tracking opportunities
- moving opportunities through the pipeline
- adding notes/interactions
- displaying dashboard stats

---

## 6.2 Apps Owned by PERSON_B

Recommended apps:

```txt
leads/
crm/
interactions/
dashboard/
```

---

## 6.3 Models Owned by PERSON_B

### Lead

Fields:

```txt
id
full_name
phone
email
budget_min
budget_max
preferences
source
created_at
updated_at
```

Lead source values:

```txt
whatsapp
referral
direct
facebook
instagram
website
other
```

### LeadPropertyInterest

Fields:

```txt
id
lead
property
interest_level
created_at
```

Interest level values:

```txt
low
medium
high
```

### PipelineStage

Fields:

```txt
id
name
slug
order
```

Default stage slugs:

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

### Opportunity

Fields:

```txt
id
lead
property
stage
status
notes
created_at
updated_at
```

Opportunity status values:

```txt
open
won
lost
```

### Interaction

Fields:

```txt
id
type
title
content
lead
property
opportunity
interaction_date
created_at
updated_at
```

Interaction type values:

```txt
call
whatsapp
visit
note
other
```

---

## 6.4 Endpoints Owned by PERSON_B

### Leads

```http
GET /api/admin/leads/
POST /api/admin/leads/
GET /api/admin/leads/{id}/
PATCH /api/admin/leads/{id}/
DELETE /api/admin/leads/{id}/
```

### Lead–Property Interests

```http
POST /api/admin/lead-property-interests/
DELETE /api/admin/lead-property-interests/{id}/
```

### Pipeline Stages

```http
GET /api/admin/pipeline-stages/
```

### Opportunities

```http
GET /api/admin/opportunities/
POST /api/admin/opportunities/
GET /api/admin/opportunities/{id}/
PATCH /api/admin/opportunities/{id}/
PATCH /api/admin/opportunities/{id}/move-stage/
DELETE /api/admin/opportunities/{id}/
```

### Interactions

```http
GET /api/admin/interactions/
POST /api/admin/interactions/
PATCH /api/admin/interactions/{id}/
DELETE /api/admin/interactions/{id}/
```

### Dashboard

```http
GET /api/admin/dashboard/overview/
GET /api/admin/dashboard/pipeline-summary/
GET /api/admin/dashboard/recent-activities/
```

`recent-activities` is optional if time is limited.

---

## 6.5 PERSON_B Must Provide

PERSON_B must provide working serializers for:

```txt
LeadListSerializer
LeadDetailSerializer
LeadCreateUpdateSerializer
LeadPropertyInterestSerializer
PipelineStageSerializer
OpportunityListSerializer
OpportunityDetailSerializer
OpportunityCreateUpdateSerializer
InteractionSerializer
DashboardOverviewSerializer if needed
```

PERSON_B must provide filters for:

Leads:

```txt
search
source
ordering
```

Opportunities:

```txt
stage
status
lead
property
```

Interactions:

```txt
lead
opportunity
property
type
```

---

## 6.6 PERSON_B Business Rules

PERSON_B owns these rules:

### Opportunity Stage Movement

Endpoint:

```http
PATCH /api/admin/opportunities/{id}/move-stage/
```

Rules:

```txt
If stage becomes sold:
- opportunity.status = won
- related property.status = sold

If stage becomes lost:
- opportunity.status = lost

If stage becomes reserved:
- related property.status = reserved

If moved back from reserved/sold:
- property status should only change if business logic allows it
- keep simple for MVP and document behavior
```

### Lead Is Not a User

A lead must never be treated as an authenticated user.

No password, no login, no account creation.

### Pipeline Stages

Default stages must be seeded automatically.

---

## 6.7 PERSON_B Must Not Implement

PERSON_B should not implement:

- auth logic
- public property browsing
- property image upload
- public settings
- WhatsApp URL generation for public property page

PERSON_B can reference the Property model owned by PERSON_A.

---

# 7. Integration Points Between PERSON_A and PERSON_B

## 7.1 Property Model Dependency

PERSON_B depends on PERSON_A’s `Property` model for:

```txt
LeadPropertyInterest.property
Opportunity.property
Interaction.property
Dashboard property stats
```

PERSON_A must keep the Property model stable after CRM work begins.

If fields change, PERSON_A must notify PERSON_B.

---

## 7.2 Property Status Updates

PERSON_B may update `Property.status` through opportunity business rules.

Expected status values:

```txt
available
reserved
sold
```

PERSON_B should not modify unrelated property fields.

---

## 7.3 Admin Property Details

PERSON_A owns:

```http
GET /api/admin/properties/{id}/
```

But this response may include `interested_leads`.

PERSON_A and PERSON_B must coordinate this field.

Simple options:

```txt
Option A: PERSON_A includes interested_leads using LeadPropertyInterest relationship.
Option B: PERSON_A returns property details only, and frontend fetches interested leads through CRM endpoints.
```

Recommended MVP choice:

```txt
Option B if speed matters. Option A if easy.
```

---

## 7.4 Dashboard

PERSON_B owns dashboard endpoints.

Dashboard may read:

```txt
Property counts from PERSON_A models
Lead counts from PERSON_B models
Opportunity counts from PERSON_B models
```

---

# 8. Development Order

## Phase 1 — PERSON_A Starts

PERSON_A should first deliver:

```txt
project setup
database connection
auth
base user/admin login
property model
property image model
public property list/detail
admin property CRUD
```

## Phase 2 — PERSON_B Starts After Property Model Exists

PERSON_B can start once `Property` model and migrations are available.

PERSON_B then delivers:

```txt
lead model
lead CRUD
lead-property interest
pipeline stages seed
opportunity model
opportunity CRUD
move-stage logic
interactions
dashboard
```

## Phase 3 — Parallel Integration

Both people verify:

```txt
all endpoints exist
response shapes match frontend contract
private endpoints require auth
public endpoints are open
dashboard counts are correct
property status updates work
```

---

# 9. Branching Recommendation

Use one branch per person.

```txt
backend/person-a-core-properties
backend/person-b-crm
```

Merge order:

```txt
1. Merge PERSON_A foundation first
2. Rebase PERSON_B branch on latest main
3. Resolve model/import conflicts
4. Merge PERSON_B CRM
```

---

# 10. Pull Request Rules

Each PR should include:

```txt
What was implemented
Endpoints added/changed
Models added/changed
Migrations added
How to test
Known limitations
```

Avoid mixing unrelated work.

---

# 11. Testing Responsibilities

## PERSON_A Tests

PERSON_A should test:

```txt
login
current user
public settings
public property list
public property detail
admin property CRUD
property image upload/delete
property filters
```

## PERSON_B Tests

PERSON_B should test:

```txt
lead CRUD
lead search/filter
lead-property interest creation/deletion
pipeline stage list
opportunity CRUD
move-stage behavior
interaction CRUD
dashboard overview
pipeline summary
```

---

# 12. API Documentation Responsibility

PERSON_A sets up the API documentation base if included.

PERSON_B documents CRM endpoints.

Both must ensure endpoint names and response shapes match the frontend–backend contract.

---

# 13. Definition of Done

A backend task is done only when:

```txt
model/migration is complete
serializer is complete
endpoint works
permissions are correct
response shape matches contract
basic validation exists
endpoint is tested manually
API docs or notes are updated
```

---

# 14. Final Backend MVP Checklist

## PERSON_A Checklist

```txt
[ ] Django project setup completed
[ ] Environment config completed
[ ] Auth endpoints completed
[ ] User/admin model completed
[ ] Public settings endpoint completed
[ ] Property model completed
[ ] Property image model completed
[ ] Public property listing completed
[ ] Public property details completed
[ ] Admin property CRUD completed
[ ] Image upload/delete completed
[ ] Property filters/search completed
[ ] WhatsApp URLs generated for public details
```

## PERSON_B Checklist

```txt
[ ] Lead model completed
[ ] Lead CRUD completed
[ ] Lead search/filter completed
[ ] Lead-property interest model completed
[ ] Interest create/delete completed
[ ] Pipeline stage model completed
[ ] Default stages seeded
[ ] Opportunity model completed
[ ] Opportunity CRUD completed
[ ] Move-stage endpoint completed
[ ] Property status update rules completed
[ ] Interaction model completed
[ ] Interaction CRUD completed
[ ] Dashboard overview completed
[ ] Pipeline summary completed
[ ] Recent activities endpoint completed if included
```

---

# 15. AI Coding Instruction Block

Use this block at the beginning of AI coding sessions.

```txt
You are helping me implement the backend of CyphX Real Estate Platform MVP.

I am: [PERSON_A_OR_PERSON_B]

Follow the Backend–Backend Contract strictly.

If I am PERSON_A:
- Work only on project setup, auth, properties, property images, public settings, and public property APIs.
- Do not implement leads, opportunities, interactions, or dashboard unless I explicitly ask.

If I am PERSON_B:
- Work only on leads, CRM, pipeline, opportunities, interactions, and dashboard.
- Do not implement auth, public property browsing, property image upload, or public settings unless I explicitly ask.

Respect the frontend–backend contract response shapes.
Do not add out-of-scope MVP features.
French and Arabic are supported.
Spanish is not implemented in MVP.
```

---

# 16. Final Note

This backend split is designed to keep the work simple.

PERSON_A builds the foundation and property catalog.

PERSON_B builds the CRM and sales tracking system.

Any change outside this contract should be discussed before implementation.
