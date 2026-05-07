"""
PERSON_B integration test — CRM & Sales endpoints.

Run with:
    python test_crm_endpoints.py

Verifies all 21 PERSON_B endpoints against the Frontend–Backend Contract.
"""

import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from rest_framework.test import APIClient
from accounts.models import User
from properties.models import Property
from leads.models import Lead, LeadPropertyInterest
from crm.models import Opportunity, PipelineStage
from interactions.models import Interaction

print("=== STARTING PERSON_B CRM ENDPOINT TESTS ===\n")

# ─── Reset ────────────────────────────────────────────────────────────────────
Interaction.objects.all().delete()
Opportunity.objects.all().delete()
LeadPropertyInterest.objects.all().delete()
Lead.objects.all().delete()
Property.objects.all().delete()
User.objects.filter(email="admin@test.com").delete()

# ─── Setup ────────────────────────────────────────────────────────────────────
user = User.objects.create_superuser(
    email="admin@test.com", password="pass1234", full_name="Test Admin"
)

# Create a test property (PERSON_A owns this model — just create directly)
prop = Property.objects.create(
    title_fr="Appartement Test",
    title_ar="شقة تجريبية",
    type="apartment",
    price=950000,
    currency="MAD",
    location_fr="Casablanca",
    status="available",
    is_public=True,
)

client = APIClient(SERVER_NAME="localhost")

# ─── 1. Login ─────────────────────────────────────────────────────────────────
resp = client.post("/api/auth/login/", {"email": "admin@test.com", "password": "pass1234"}, format="json")
assert resp.status_code == 200, f"Login failed: {resp.content}"
token = resp.data["access"]
client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
print("[OK] Login OK")

# ─── 2. Pipeline stages are seeded ────────────────────────────────────────────
resp = client.get("/api/admin/pipeline-stages/")
assert resp.status_code == 200, f"Pipeline stages failed: {resp.content}"
stages = resp.data
assert len(stages) == 8, f"Expected 8 stages, got {len(stages)}"
slugs = [s["slug"] for s in stages]
for expected in ["new_lead", "contacted", "interested", "visit_planned", "negotiation", "reserved", "sold", "lost"]:
    assert expected in slugs, f"Missing stage slug: {expected}"
print(f"[OK] Pipeline stages seeded correctly ({len(stages)} stages)")

# ─── 3. Create a lead ─────────────────────────────────────────────────────────
lead_data = {
    "full_name": "Youssef Amrani",
    "phone": "+212600000001",
    "email": "youssef@example.com",
    "budget_min": 700000,
    "budget_max": 1000000,
    "preferences": "Wants garage and elevator.",
    "source": "whatsapp",
}
resp = client.post("/api/admin/leads/", lead_data, format="json")
assert resp.status_code == 201, f"Create lead failed: {resp.content}"
lead_id = resp.data["id"]
assert resp.data["full_name"] == "Youssef Amrani"
print(f"[OK] Lead created (id={lead_id})")

# ─── 4. List leads ────────────────────────────────────────────────────────────
resp = client.get("/api/admin/leads/")
assert resp.status_code == 200 and resp.data["count"] == 1, f"List leads failed: {resp.content}"
print("[OK] Lead list OK")

# ─── 5. Lead detail ───────────────────────────────────────────────────────────
resp = client.get(f"/api/admin/leads/{lead_id}/")
assert resp.status_code == 200, f"Lead detail failed: {resp.content}"
assert "interested_properties" in resp.data
assert "opportunities" in resp.data
assert "recent_interactions" in resp.data
print("[OK] Lead detail OK (nested fields present)")

# ─── 6. Filter leads by source ────────────────────────────────────────────────
resp = client.get("/api/admin/leads/?source=whatsapp")
assert resp.status_code == 200 and resp.data["count"] == 1
resp2 = client.get("/api/admin/leads/?source=referral")
assert resp2.status_code == 200 and resp2.data["count"] == 0
print("[OK] Lead source filter OK")

# ─── 7. Update lead ───────────────────────────────────────────────────────────
resp = client.patch(f"/api/admin/leads/{lead_id}/", {"budget_max": 1200000}, format="json")
assert resp.status_code == 200 and resp.data["budget_max"] == "1200000.00", f"Update lead failed: {resp.content}"
print("[OK] Lead PATCH OK")

# ─── 8. Create lead–property interest ─────────────────────────────────────────
resp = client.post("/api/admin/lead-property-interests/", {
    "lead_id": lead_id, "property_id": prop.id, "interest_level": "high"
}, format="json")
assert resp.status_code == 201, f"Create interest failed: {resp.content}"
interest_id = resp.data["id"]
assert resp.data["interest_level"] == "high"
assert resp.data["lead"]["id"] == lead_id
assert resp.data["property"]["id"] == prop.id
print(f"[OK] LeadPropertyInterest created (id={interest_id})")

# ─── 9. Duplicate interest returns 400 ────────────────────────────────────────
resp = client.post("/api/admin/lead-property-interests/", {
    "lead_id": lead_id, "property_id": prop.id, "interest_level": "low"
}, format="json")
assert resp.status_code == 400, f"Expected 400 for duplicate, got {resp.status_code}"
print("[OK] Duplicate interest correctly rejected (400)")

# ─── 10. Lead detail now shows interested property ────────────────────────────
resp = client.get(f"/api/admin/leads/{lead_id}/")
assert len(resp.data["interested_properties"]) == 1
print("[OK] Lead detail shows interested property")

# ─── 11. Create opportunity ───────────────────────────────────────────────────
new_lead_stage = next(s for s in stages if s["slug"] == "new_lead")
resp = client.post("/api/admin/opportunities/", {
    "lead_id": lead_id, "property_id": prop.id,
    "stage_id": new_lead_stage["id"], "notes": "Initial contact via WhatsApp."
}, format="json")
assert resp.status_code == 201, f"Create opportunity failed: {resp.content}"
opp_id = resp.data["id"]
assert resp.data["status"] == "open"
print(f"[OK] Opportunity created (id={opp_id})")

# ─── 12. Move stage -> reserved ────────────────────────────────────────────────
reserved_stage = next(s for s in stages if s["slug"] == "reserved")
resp = client.patch(f"/api/admin/opportunities/{opp_id}/move-stage/",
    {"stage_id": reserved_stage["id"]}, format="json")
assert resp.status_code == 200, f"Move stage failed: {resp.content}"
assert resp.data["stage"]["slug"] == "reserved"
prop.refresh_from_db()
assert prop.status == "reserved", f"Expected property reserved, got {prop.status}"
print("[OK] Move stage -> reserved; property.status = reserved OK")

# ─── 13. Move stage -> sold ────────────────────────────────────────────────────
sold_stage = next(s for s in stages if s["slug"] == "sold")
resp = client.patch(f"/api/admin/opportunities/{opp_id}/move-stage/",
    {"stage_id": sold_stage["id"]}, format="json")
assert resp.status_code == 200, f"Move to sold failed: {resp.content}"
assert resp.data["status"] == "won"
prop.refresh_from_db()
assert prop.status == "sold", f"Expected property sold, got {prop.status}"
print("[OK] Move stage -> sold; opportunity.status = won, property.status = sold OK")

# ─── 14. Move stage -> lost (reset status to lost) ─────────────────────────────
lost_stage = next(s for s in stages if s["slug"] == "lost")
resp = client.patch(f"/api/admin/opportunities/{opp_id}/move-stage/",
    {"stage_id": lost_stage["id"]}, format="json")
assert resp.status_code == 200
assert resp.data["status"] == "lost"
print("[OK] Move stage -> lost; opportunity.status = lost OK")

# ─── 15. Move back to contacted (status resets to open) ───────────────────────
contacted_stage = next(s for s in stages if s["slug"] == "contacted")
resp = client.patch(f"/api/admin/opportunities/{opp_id}/move-stage/",
    {"stage_id": contacted_stage["id"]}, format="json")
assert resp.status_code == 200
assert resp.data["status"] == "open"
print("[OK] Move back -> contacted; opportunity.status = open OK")

# ─── 16. Create interaction ───────────────────────────────────────────────────
from datetime import datetime, timezone
resp = client.post("/api/admin/interactions/", {
    "type": "call",
    "title": "First call",
    "content": "Client asked about payment options.",
    "lead_id": lead_id,
    "property_id": prop.id,
    "opportunity_id": opp_id,
    "interaction_date": "2026-05-07T10:00:00Z",
}, format="json")
assert resp.status_code == 201, f"Create interaction failed: {resp.content}"
interaction_id = resp.data["id"]
assert resp.data["lead"]["id"] == lead_id
assert resp.data["property"]["id"] == prop.id
print(f"[OK] Interaction created (id={interaction_id})")

# ─── 17. Filter interactions by lead ──────────────────────────────────────────
resp = client.get(f"/api/admin/interactions/?lead={lead_id}")
assert resp.status_code == 200 and resp.data["count"] == 1
resp2 = client.get(f"/api/admin/interactions/?type=visit")
assert resp2.status_code == 200 and resp2.data["count"] == 0
print("[OK] Interaction filters (lead, type) OK")

# ─── 18. Update interaction ───────────────────────────────────────────────────
resp = client.patch(f"/api/admin/interactions/{interaction_id}/",
    {"content": "Client confirmed interest."}, format="json")
assert resp.status_code == 200 and "confirmed" in resp.data["content"]
print("[OK] Interaction PATCH OK")

# ─── 19. Dashboard overview ───────────────────────────────────────────────────
resp = client.get("/api/admin/dashboard/overview/")
assert resp.status_code == 200, f"Dashboard overview failed: {resp.content}"
data = resp.data
assert "properties" in data and "leads" in data and "opportunities" in data
assert data["properties"]["total"] == 1
assert data["leads"]["total"] == 1
assert data["opportunities"]["total"] == 1
print(f"[OK] Dashboard overview OK (props={data['properties']['total']}, leads={data['leads']['total']}, opps={data['opportunities']['total']})")

# ─── 20. Dashboard pipeline summary ──────────────────────────────────────────
resp = client.get("/api/admin/dashboard/pipeline-summary/")
assert resp.status_code == 200, f"Pipeline summary failed: {resp.content}"
assert isinstance(resp.data, list) and len(resp.data) == 8
contacted_row = next(r for r in resp.data if r["stage"]["slug"] == "contacted")
assert contacted_row["count"] == 1, f"Expected 1 open opp in contacted, got {contacted_row['count']}"
print("[OK] Dashboard pipeline summary OK")

# ─── 21. Recent activities ────────────────────────────────────────────────────
resp = client.get("/api/admin/dashboard/recent-activities/")
assert resp.status_code == 200 and len(resp.data) >= 1
assert resp.data[0]["type"] == "interaction"
print("[OK] Dashboard recent activities OK")

# ─── 22. Auth check — all endpoints reject unauthenticated requests ───────────
anon = APIClient(SERVER_NAME="localhost")
endpoints = [
    ("GET",    "/api/admin/leads/"),
    ("GET",    "/api/admin/pipeline-stages/"),
    ("GET",    "/api/admin/opportunities/"),
    ("GET",    "/api/admin/interactions/"),
    ("GET",    "/api/admin/dashboard/overview/"),
    ("GET",    "/api/admin/dashboard/pipeline-summary/"),
]
for method, path in endpoints:
    r = getattr(anon, method.lower())(path)
    assert r.status_code == 401, f"Expected 401 for anon {method} {path}, got {r.status_code}"
print(f"[OK] All {len(endpoints)} tested endpoints correctly reject unauthenticated requests (401)")

# ─── 23. Delete interest ─────────────────────────────────────────────────────
resp = client.delete(f"/api/admin/lead-property-interests/{interest_id}/")
assert resp.status_code == 200 and "deleted" in resp.data["detail"]
print("[OK] Interest deleted OK")

# ─── 24. Delete interaction ──────────────────────────────────────────────────
resp = client.delete(f"/api/admin/interactions/{interaction_id}/")
assert resp.status_code == 200
print("[OK] Interaction deleted OK")

# ─── 25. Delete opportunity ──────────────────────────────────────────────────
resp = client.delete(f"/api/admin/opportunities/{opp_id}/")
assert resp.status_code == 200 and "deleted" in resp.data["detail"]
print("[OK] Opportunity deleted OK")

# ─── 26. Delete lead ─────────────────────────────────────────────────────────
resp = client.delete(f"/api/admin/leads/{lead_id}/")
assert resp.status_code == 200 and "deleted" in resp.data["detail"]
print("[OK] Lead deleted OK")

print("\n=== ALL PERSON_B CRM TESTS PASSED OK ===")
