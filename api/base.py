import requests
import urllib3

from config import STAGE_AUTH_TOKEN, STAGE_URL

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BaseApiStage:
    def __init__(self):
        self.base_url = STAGE_URL
        self.timeout = 5
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            "Authorization": STAGE_AUTH_TOKEN,
            "Content-type": "application/json",
        })


    def _url(self, path):
        return f"{self.base_url}/etisalat/v1/{path}"


    def create_sub(self, email, plan_id, quantity, accountId="null", method="POST"):
        return self.session.request(
            method,
            self._url("/subscriptions"),
            json={
                "emailAddress": email,
                "planId": plan_id,
                "quantity": quantity,
                "accountId": accountId,
            },
            timeout=self.timeout
        )


    def create_sub_raw(self, **fields):
        return self.session.post(
            self._url("/subscriptions"),
            json=fields,
            timeout=self.timeout
        )


    def get_subscription(self, sub_id, method="GET"):
        return self.session.request(
            method,
            self._url(f"/subscriptions/{sub_id}"),
            timeout=self.timeout
            )


    def change_quantity(self, sub_id, quantity, is_forse=True,method="POST"):
        return self.session.request(
            method,
            self._url(f"/subscriptions/{sub_id}/quantity"),
            json={
                "quantity": quantity,
                "isForce": is_forse,
            }
        )


    def cancel_sub(self, sub_id, reason="cancel",method="POST"):
        return self.session.request(
            method,
            self._url(f"subscriptions/{sub_id}/cancel"),
            json={
                "reason": reason
            },
            timeout=self.timeout,
        )