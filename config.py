# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DISK_OAUTH_TOKEN = os.getenv("DISK_OAUTH_TOKEN")
DISK_BASE_URL = os.getenv("DISK_BASE_URL", "https://cloud-api.yandex.net/v1/disk")
TEST_FOLDER = "/test_automation"
