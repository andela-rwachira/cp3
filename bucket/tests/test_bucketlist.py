import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class BucketlistAPIView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='pass')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_new_bucketlist(self):
        """Tests a new bucketlist can be added."""
        response = self.client.post('/bucketlists/', {'title': 'bucketlist'},
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.data, {'title': 'Bucketlist'})
