import os

from .base import *

# azure storage config
DEFAULT_FILE_STORAGE = "core.storage.AzureMediaStorage"
STATICFILES_STORAGE = "core.storage.AzureStaticStorage"


AZURE_ACCOUNT_NAME = os.environ.get("AZURE_ACCOUNT_NAME")
AZURE_CUSTOM_DOMAIN = os.environ.get("AZURE_CUSTOM_DOMAIN")
AZURE_URL_EXPIRATION_SECS = 300
STATICFILES_LOCATION = "static"
MEDIAFILES_LOCATION = "media"
