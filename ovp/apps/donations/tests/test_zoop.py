import os

from django.test import TestCase
from django.test.utils import override_settings
from ovp.apps.donations.backends.zoop import ZoopBackend


@override_settings(ZOOP_MARKETPLACE_ID=os.environ.get('ZOOP_MARKETPLACE_ID', None),
                   ZOOP_PUB_KEY=os.environ.get('ZOOP_PUB_KEY', None))
class TestZoopBackend(TestCase):
  def setUp(self):
    self.backend = ZoopBackend()

  def test_generate_card_token(self):
    response = self.backend.generate_card_token(holder_name="Test", expiration_month="03", expiration_year="2018", security_code="123", card_number="5201561050024014")
    self.assertEqual(response.status_code, 201)
    self.assertTrue(response.json()["id"])

  def test_charge_card(self):
    token = self.backend.generate_card_token(holder_name="Test", expiration_month="03", expiration_year="2018", security_code="123", card_number="5201561050024014")
    token_id = token.json()["id"]
    response = self.backend.charge(token_id)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()["status"], "succeeded")

class TestSettinglessZoopBackend(TestCase):
  def test_require_settings(self):
    with self.assertRaises(AssertionError):
      backend = ZoopBackend()