import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserAPIView(APITestCase):
    """
    """
    def setUp(self):
        self.url = '/auth/register'
        self.user_data = {'username': 'testjane',
                          'password': 'testpass'}

    def tearDown(self):
        del self.user_data

    def test_register_new_user(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.get().username, 'testjane')

    def test_invalid_registration(self):
        pass


class UserLoginView(APITestCase):
    """
    """
    def setUp(self):
        self.url = '/auth/login'
        self.user_data = {'username': 'testjane',
                          'password': 'testpass'}
        self.bad_data1 = {'username': 'invalid',
                          'password': 'testpass'}
        self.bad_data2 = {'username': 'testjane',
                          'password': 'invalid'}
        self.user = self.client.post(self.url, self.user_data)

    def tearDown(self):
        del self.user

    def test_login(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, 200)
        # self.assertTrue(response.data['token'])

    def test_invalid_username_login(self):
        response = self.client.post(self.url, self.bad_data1)
        self.assertEqual(response.status_code, 400)

    def test_invalid_password_login(self):
        response = self.client.post(self.url, self.bad_data2)
        self.assertEqual(response.status_code, 400)
