from .base import *  # noqa

CELERY_ALWAYS_EAGER = True
DEBUG = False
TEMPLATES[0]["OPTIONS"]["debug"] = False  # noqa
DEFAULT_PASSWORD = "12345"
