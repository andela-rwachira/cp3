from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class UserRegistrationAPIView(APITestCase):
    """
    Test new user registration.
    """

    def setUp(self):
        self.url = '/api/auth/register'

    def test_register_new_user(self):
        """Tests a new user can be succesfully registered."""
        self.user_data = {'username': 'testjane',
                          'password': 'testpass'}

        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.get().username, 'testjane')

    def test_duplicate_registration(self):
        """Tests error raised when creating duplicate users."""
        self.duplicate_user = User.objects.create_user(username='testjoe',
                                                       password='testpassjoe')

        response = self.client.post(self.url, {'username': 'testjoe',
                                               'password': 'testpassjoe'})
        self.assertEqual(response.status_code, 400)


class UserLoginAPIView(APITestCase):
    """
    Test user login.
    """

    def setUp(self):
        """Create a dummy user to test login against."""
        self.url = '/api/auth/login'
        User.objects.create_user(username='testjane', password='testpass')

    def test_login(self):
        """Tests token generated on succesfull login."""
        self.user_data = {'username': 'testjane',
                          'password': 'testpass'}

        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

    def test_invalid_username_login(self):
        """Tests error raised when username is invalid."""
        self.bad_data1 = {'username': 'invalid',
                          'password': 'testpass'}

        response = self.client.post(self.url, self.bad_data1)
        self.assertEqual(response.status_code, 400)

    def test_invalid_password_login(self):
        """Tests error raised when password is invalid."""
        self.bad_data2 = {'username': 'testjane',
                          'password': 'invalid'}

        response = self.client.post(self.url, self.bad_data2)
        self.assertEqual(response.status_code, 400)
