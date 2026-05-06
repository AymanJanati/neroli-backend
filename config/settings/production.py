from .base import *  # noqa

DEBUG = False

# In production set ALLOWED_HOSTS via environment variable
# ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
