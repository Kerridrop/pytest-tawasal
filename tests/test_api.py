import pytest

from config import CHANGE_QUANTITY, TEST_EMAIL_CREATE, PLANS, VALID_BODY_CREATE
from api.base import BaseApiStage


class TestSubscriptionQuantity:

    @pytest.mark.parametrize(
        "method, expected_status",
        [
            ("HEAD", 405),
            ("OPTIONS", 405),
            ("PUT", 405),
            ("DELETE", 405),
            ("PATCH", 405),
            ("GET", 200),
       ],
    )
    def test_get_method_validation(self, method, api, subscription,expected_status):
        sub_id = subscription["subscriptionID"]

        response = api.get_subscription(sub_id, method)
        assert response.status_code == expected_status, (f"Expecting {expected_status}, got: {response.status_code}")


    def test_quantity_check(self, subscription):
        assert subscription["quantity"] > 0


    def test_quantity_change(self, api, subscription):
        sub_id = subscription["subscriptionID"]

        response = api.change_quantity(sub_id, CHANGE_QUANTITY)

        assert response.status_code == 200, f"Change error: {response.text[:50]}"
        assert response.json()["allowed"] is True

        check = api.get_subscription(sub_id)
        assert check.status_code == 200, f"Get info error: {check.text[:50]}"
        assert check.json()["quantity"] == CHANGE_QUANTITY, f"Not applied: {check.text[:50]}"


    @pytest.mark.parametrize("method, expected_status",[
            ("HEAD", 405),
            ("OPTIONS", 405),
            ("PUT", 405),
            ("DELETE", 405),
            ("PATCH", 405),
            ("GET", 200),
            ("POST", 201),
        ],
    )
    def test_onboarding_methods(self, api, method, expected_status):
        response = api.create_sub(email="tawasaltestqa+autotest@gmail.com", plan_id=PLANS["Pro"], quantity=5,accountId="null",method=method)

        if response.status_code == 201:
            api.cancel_sub(response.json()["subscriptionID"])

        assert response.status_code == expected_status, \
            f"{method}: expecting {expected_status}, got {response.status_code}"


    @pytest.mark.parametrize("method, expected_status",[
            ("HEAD", 405),
            ("OPTIONS", 405),
            ("PUT", 405),
            ("DELETE", 405),
            ("PATCH", 405),
            ("POST", 405),
        ]
    )
    def test_check_id_methods(self, api, method,expected_status, subscription):
        sub_id = subscription["subscriptionID"]

        response = api.get_subscription(sub_id, method)
        assert response.status_code == expected_status, \
            f"{method}: expecting {expected_status}, got {response.status_code}"


    @pytest.mark.parametrize("method, expected_status",[
            ("HEAD", 405),
            ("OPTIONS", 405),
            ("PUT", 405),
            ("DELETE", 405),
            ("PATCH", 405),
            pytest.param(
                "GET", 405,
                marks=pytest.mark.xfail(
                reason="Wrong status 200 with HTML body")
            )
        ]
    )
    def test_cancel_methods(self, api, method,expected_status ,subscription):
        sub_id = subscription["subscriptionID"]

        response = api.cancel_sub(sub_id, reason="cancel", method=method)
        assert response.status_code == expected_status, \
            f"{method}: expecting {expected_status}, got {response.status_code}"


# === negative scenatios ===

@pytest.mark.parametrize("field",[
        "emailAddress",
        "planId",
        "quantity",
        "accountId",
    ], ids=[
        "without_email",
        "without_plan",
        "without_quantity",
        "without accountId",
    ]
)
@pytest.mark.parametrize("case",[
        "missing",
        "null",
    ]
)
def test_create_without_required_field(api, field, case):
    body = VALID_BODY_CREATE.copy()

    if case == "missing":
        del body[field]
    else:
        body[field] = None

    response = api.create_sub_raw(**body)
    assert response.status_code == 400, f"Field{field}({case}: expecting 400, got {response.status_code})"
