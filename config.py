import os
from dotenv import load_dotenv


load_dotenv()


STAGE_URL = os.environ["STAGE_URL"]

STAGE_AUTH_TOKEN = os.environ["STAGE_TOKEN"]

CHANGE_QUANTITY = 10

PAYLOAD1 = {"emailAddress": "tawasaltestqa@gmail.com"}

TEST_EMAIL = "tawasaltestqa@gmail.com"

TEST_EMAIL_CREATE = "tawasaltestqa+autotest@gmail.com"

PLANS = {
    "Base": "basic",
    "Pro": "with_aleria_pro"
}

