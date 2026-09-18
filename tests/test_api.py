import pytest

from config import CHANGE_QUANTITY, TEST_EMAIL_CREATE, PLANS, VALID_BODY_CREATE
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
