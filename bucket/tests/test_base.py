from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from bucket.models import Bucketlist, Item


class BaseTestCase(APITestCase):
    """
    A base test case which creates dummy
    user, bucketlist and bucketlist item db entries.
    """

    def setUp(self):
      # create test user and retrieve token
        self.user = User.objects.create_user(username='user',
                                             password='pass')
        self.url_login = '/api/auth/login'
        self.user_data = {'username': 'user',
                          'password': 'pass'}
        response = self.client.post(self.url_login, self.user_data)
        self.token = response.data['token']

        # create test bucketlists
        self.bucketlist = Bucketlist.objects.create(name='testbucketlist',
                                                    created_by=self.user)
        self.bucketlist2 = Bucketlist.objects.create(name='testbucketlist2',
                                                     created_by=self.user)
        # create test items
        self.item = Item.objects.create(name='testitem',
                                        created_by=self.user,
                                        bucket=self.bucketlist)
        self.item2 = Item.objects.create(name='testitem2',
                                         created_by=self.user,
                                         bucket=self.bucketlist)
        self.api_authentication()

    def api_authentication(self):
        """Sets auth header for all requests."""
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.token)
