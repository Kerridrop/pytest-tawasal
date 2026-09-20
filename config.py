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

VALID_BODY_CREATE = {
    "emailAddress": TEST_EMAIL_CREATE,
    "planId": PLANS["Pro"],
    "quantity": 5,
    "accountId": "null",
}

INVALID_VALUES = [
    ("emailAddress", "not-an-email", 400),
    ("emailAddress", "", 400),
    ("emailAddress", 123, 400),
    ("planId", "nonexistent_plan", 400),
    ("planId", "", 400),
    ("planId", 123, 400),
    ("quantity", 0, 409),
    ("quantity", -1, 409),
    ("quantity", 1.5, 400),
    ("quantity", "five", 400),
    ("accountId", 123, 400),
]