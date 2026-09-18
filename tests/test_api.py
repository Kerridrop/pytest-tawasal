import pytest
import requests

from config import CHANGE_QUANTITY, TEST_EMAIL_CREATE, PLANS
from api.base import BaseApiStage


class TestSubscriptionQuantity:

    def test_quantity_check(self,api,  subscription):
        assert subscription["quantity"] > 0


    def test_quantity_change(self, api, subscription):
        sub_id = subscription["subscriptionID"]

        response = api.change_quantity(sub_id, CHANGE_QUANTITY)

        assert response.status_code == 200, f"Change error: {response.text[:50]}"
        assert response.json()["allowed"] is True

        check = api.get_subscription(sub_id)
        assert check.status_code == 200, f"Get info error: {check.text[:50]}"
        assert check.json()["quantity"] == CHANGE_QUANTITY, f"Not applied: {check.text[:50]}"


# === negative scenatios ===

def test_empty_value(api):
    response = api.create_sub(None, None, None)
    assert response.status_code == 400,f"Created with empty values: {response.text[:50]}"


def test_value_missing_email(api):
    response = api.create_sub(None, PLANS["Pro"], 5)
    assert response.status_code == 400,f"Created with missing value email: {response.text[:50]}"


def test_value_missing_plan(api):
    response = api.create_sub(TEST_EMAIL_CREATE, None, 5)
    assert response.status_code == 400, f"Created with missing value plan: {response.text[:50]}"


def test_value_missing_quantity(api):
    response = api.create_sub(TEST_EMAIL_CREATE, PLANS["Pro"], None)
    assert response.status_code == 400, f"Created with missing value quantity: {response.text[:50]}"


def test_missing_key_email(api):
    response = api.create_sub_raw(planId=PLANS["Pro"], quantity=5, accountId="null")
    assert response.status_code == 400, f"Created with missing key email: {response.text[:50]}"


def test_missing_key_plan(api):
    response = api.create_sub_raw(emailAddress=TEST_EMAIL_CREATE, quantity=5, accountId="null")
    assert response.status_code == 400, f"Created with missing key plan: {response.text[:20]}"


def test_missing_key_quantity(api):
    response = api.create_sub_raw(emailAddress=TEST_EMAIL_CREATE, planId=PLANS["Pro"], accountId="null")
    assert response.status_code == 400,f"Created with missing key quantity: {response.text[:50]}"


def test_missing_key_account(api):
    response = api.create_sub_raw(emailAddress=TEST_EMAIL_CREATE, planId=PLANS["Pro"], quantity=5)
    assert response.status_code == 400, f"Created with missing key accountId: {response.text[:50]}"