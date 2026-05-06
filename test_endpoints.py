import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

import sys
import json
from rest_framework.test import APIClient
from accounts.models import User
from properties.models import Property
from core.models import PublicSettings

print("=== STARTING ENDPOINT TEST ===")

# Reset DB for tests
User.objects.all().delete()
Property.objects.all().delete()
PublicSettings.objects.all().delete()

# Set up test user
test_email = "admin@example.com"
test_pw = "password123"
user = User.objects.create_superuser(email=test_email, password=test_pw, full_name="Admin User")
print("[+] Created admin user.")

client = APIClient(SERVER_NAME="localhost")

# 1. Test Login
response = client.post("/api/auth/login/", {"email": test_email, "password": test_pw}, format='json')
if response.status_code != 200:
    print(f"[-] Login failed: {response.content}")
    sys.exit(1)
print("[+] Login successful.")
access_token = response.data["access"]
client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

# 2. Test Me Endpoint
response = client.get("/api/auth/me/")
if response.status_code != 200:
    print(f"[-] /api/auth/me/ failed: {response.content}")
    sys.exit(1)
print(f"[+] /auth/me/ successful. User is {response.data.get('full_name')}")

# 3. Test Public Settings
response = client.get("/api/public/settings/")
if response.status_code != 200:
    print(f"[-] /api/public/settings/ failed: {response.content}")
    sys.exit(1)
print(f"[+] Public settings loaded. WhatsApp: {response.data.get('whatsapp_phone')}")

# 4. Create Property (Admin API)
prop_data = {
    "title_fr": "Belle Villa à Marrakech",
    "title_ar": "فيلا جميلة بمراكش",
    "type": "villa",
    "price": "2500000.00",
    "currency": "MAD",
    "location_fr": "Marrakech",
    "surface": 350.5,
    "rooms": 5,
    "status": "available",
    "is_public": True
}
response = client.post("/api/admin/properties/", prop_data, format='json')
if response.status_code != 201:
    print(f"[-] Create property failed: {response.content}")
    sys.exit(1)
prop_id = response.data["id"]
print(f"[+] Created property ID {prop_id} via Admin API.")

# 5. List Admin Properties
response = client.get("/api/admin/properties/")
if response.status_code != 200 or response.data["count"] != 1:
    print(f"[-] List admin properties failed: {response.content}")
    sys.exit(1)
print("[+] Listed admin properties successfully.")

# 6. Update Property (Admin API)
response = client.patch(f"/api/admin/properties/{prop_id}/", {"status": "reserved"}, format='json')
if response.status_code != 200:
    print(f"[-] Update property failed: {response.content}")
    sys.exit(1)
print(f"[+] Updated property status to {response.data['status']}.")

# 7. List Public Properties
# Log out client to test public access
public_client = APIClient(SERVER_NAME="localhost")
response = public_client.get("/api/public/properties/?city=Marrakech&type=villa&status=reserved")
if response.status_code != 200 or response.data["count"] != 1:
    print(f"[-] List public properties filters failed: {response.content}")
    sys.exit(1)
print(f"[+] Public list with filters matched {response.data['count']} properties.")

# 8. Get Public Property Detail & Verify WhatsApp URL
response = public_client.get(f"/api/public/properties/{prop_id}/")
if response.status_code != 200:
    print(f"[-] Get public property detail failed: {response.content}")
    sys.exit(1)

whatsapp_data = response.data.get("whatsapp")
if not whatsapp_data or "https://wa.me/212600000000" not in whatsapp_data.get("contact_url_fr", ""):
    print(f"[-] WhatsApp URLs missing or incorrect: {whatsapp_data}")
    sys.exit(1)
print("[+] Public property details retrieved, WhatsApp URLs perfectly generated.")

# 9. Delete Property (Admin API)
response = client.delete(f"/api/admin/properties/{prop_id}/")
if response.status_code != 200:
    print(f"[-] Delete property failed: {response.content}")
    sys.exit(1)
print("[+] Property deleted successfully.")

print("=== ALL TESTS PASSED SUCCESSFULLY! ===")
