import requests
from django.conf import settings
from ovp.apps.donations.backends.base import BaseBackend

POST="post"
GET="get"
PATCH="patch"
PUT="put"
DELETE="delete"

class ZoopBackend(BaseBackend):
  def __init__(self):
    self.marketplace_id = getattr(settings, "ZOOP_MARKETPLACE_ID", None)
    self.pub_key = getattr(settings, "ZOOP_PUB_KEY", None)
    self.seller_id = getattr(settings, "ZOOP_SELLER_ID", None)
    self.statement_descriptor = getattr(settings, "ZOOP_STATEMENT_DESCRIPTOR", None)
    
    assert (self.marketplace_id and self.pub_key and 
            self.seller_id and self.statement_descriptor)

  def _build_url(self, resource):
    return "https://api.zoop.ws/" + resource.format(mpid=self.marketplace_id)

  def call(self, http_method, resource, data):
    call_method = getattr(requests, http_method)
    url = self._build_url(resource)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return call_method(url, json=data, auth=(self.pub_key, ''), headers=headers)

  def generate_card_token(self,
                          holder_name=None,
                          expiration_month=None,
                          expiration_year=None,
                          security_code=None,
                          card_number=None):
    """"
      This method is not used on test only, not on production. This API call should be done from the front-end and the token passed to subsequent calls.
    """ 
    data = {
      "holder_name": holder_name,
      "expiration_month": expiration_month,
      "expiration_year": expiration_year,
      "security_code": security_code,
      "card_number": card_number
    }
    return self.call(POST, "v1/marketplaces/{mpid}/cards/tokens", data)

  def charge(self, token, amount):
    data = {
      "payment_type": "credit",
      "currency": "BRL",
      "description": "donation",
      "amount": 100,
      "on_behalf_of": self.seller_id,
      "statement_descriptor": self.statement_descriptor,
      "token": token
    }
    response = self.call(POST, "v1/marketplaces/{mpid}/transactions", data)
    try:
      response_data = response.json()
    except:
      pass

    if response.status_code in [200, 201]:
      return (response.status_code, {"status": "succeeded", "message": "Transaction was authorized."}, response)

    if response.status_code in [400, 401]:
      return (response.status_code, {"status": "failed", "message": "An internal error occurred during processing."}, response)

    if response.status_code == 402:
      return (response.status_code, {"status": "failed", "message": response_data["error"]["message"], "category": response_data["error"]["category"]}, response)

    if response.status_code == 404:
      return (response.status_code, {"status": "failed", "message": response_data["error"]["message"], "category": response_data["error"]["category"]}, response)

    if response.status_code == 408:
      return (response.status_code, {"status": "timeout", "message": response_data["error"]["message"], "category": response_data["error"]["category"]}, response)
    
    if response.status_code in [403, 500, 502]:
      return (500, {"status": "error", "message": "Internal error occurred. This issue is being investigated."}, response)

    return (500, {"status": "error", "message": "An unexpected error occurred. This issue is being investigated."}, response)