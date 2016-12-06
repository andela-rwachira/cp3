import json
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from tests.test_base import BaseTestCase


class APIAuthTests(BaseTestCase):
    """
    Test user creation and authentication.
    """
    def login_new_user(self):
        token = Token.objects.create(username='testuser', password='pass')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.client.post(username='testjane',
                         password='jtest')