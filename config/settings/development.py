from .base import *  # noqa

DEBUG = True

# More verbose errors in dev
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True
