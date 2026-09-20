import pytest

from config import CHANGE_QUANTITY, TEST_EMAIL_CREATE, PLANS, VALID_BODY_CREATE, INVALID_VALUES
from api.base import BaseApiStage


class TestSubscriptionQuantity:

    def test_quantity_check(self, subscription):
        assert subscription["quantity"] > 0


    def test_quantity_change(self, api, subscription):
        sub_id = subscription["subscriptionID"]

        response = api.change_quantity(sub_id, CHANGE_QUANTITY)

        assert response.status_code == 200, \
            f"Change error: {response.text[:50]}"
        assert response.json()["allowed"] is True

        check = api.get_subscription(sub_id)
        assert check.status_code == 200, f"Get info error: {check.text[:50]}"
        assert check.json()["quantity"] == CHANGE_QUANTITY, \
            f"Not applied: {check.text[:50]}"

    def test_validate_sub_methods(self, api):
        response = api.validate_sub(email=TEST_EMAIL_CREATE, method="POST")

        data = response.json()
        assert data["used"] is False, \
            f"Subscription is used without activating, got {data["used"]}"


    def test_change_plan(self, api, subscription):
        sub_id = subscription["subscriptionID"]

        response = api.change_plan(sub_id=sub_id, plan=PLANS["Base"], method="POST")

        assert response.status_code == 200, \
            f"Changing error: {response.status_code}, expecting 200"
        assert response.text == "", \
            f"Got different body {response.text[:50]}"


# === negative scenatios ===

class TestMethodValidation:

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
    def test_validate_sub_methods(self, api, method, expected_status):
        response = api.validate_sub(email=TEST_EMAIL_CREATE, method=method)
        assert response.status_code == expected_status, \
            f"{method}: expecting {expected_status}, got {response.status_code}"


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
        assert response.status_code == expected_status, \
            (f"Expecting {expected_status}, got: {response.status_code}")        


@pytest.mark.parametrize(
        "field, value, expected", INVALID_VALUES,
        ids=[f"{field}={value!r}" for field, value, _ in INVALID_VALUES] #tip тут кстати есть интересность - "_" в перечислении аргументов цикла обозначается как ненужное значение
)
def test_onboarding_invalid_value(api, field, value, expected):
    body = {**VALID_BODY_CREATE, field: value}

    response = api.create_sub_raw(**body)

    if response.status_code in (200, 201):
        api.cancel_sub(response.json()["subscriptionID"])

    assert response.status_code == expected, \
        f"{field}={value!r}: expected 400, got {response.status_code}: {response.text[:50]}"


def test_nonexisting_sub(api):
    sub_id = 500

    response = api.get_subscription(sub_id)
    assert response.status_code == 404, \
        f"{response.status_code} got, expecting 404"


def test_double_cancel(api):
    create = api.create_sub(TEST_EMAIL_CREATE, PLANS["Pro"], quantity=5)
    assert create.status_code == 201, \
        f"creating failed {create.text[:100]}"
    sub_id = create.json()["subscriptionID"]

    deletefirst = api.cancel_sub(sub_id)
    assert deletefirst.status_code == 200, \
        f"Failed first deletion {deletefirst.text[:100]}"

    deletesecond = api.cancel_sub(sub_id)
    assert deletesecond.status_code == 404, \
        f"{deletesecond.status_code} gor for double deletion, expecting 404"      

        

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
    assert response.status_code == 400, \
        f"Field{field}({case}: expecting 400, got {response.status_code})"
