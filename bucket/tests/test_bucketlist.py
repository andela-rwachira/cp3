from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from bucket.models import Bucketlist


class TestBucketlistAPIView(APITestCase):
    """
    Test bucketlist interactions.
    """
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='pass')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_new_bucketlist(self):
        """Tests a new bucketlist can be added."""
        response = self.client.post('/api/bucket/', {'name': 'bucketlist'},
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'detail': 'bucketlist'})
        # asserts that the bucketlist has been crated in the db
        self.assertTrue(Bucketlist.objects.filter(name='bucketlist'))

    def test_return_all_bucketlists(self):
        """Tests retrieval of all bucketlists."""
        response = self.client.get('/api/bucket/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlist(self):
        """
        Tests retrieval of a single bucketlist.
        Two test bucketlists were added in the setUp to
        test that the id parameter works correctly.
        """
        response = self.client.get('/api/bucket/1/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'detail': 'testbucketlist'})

    def test_update_bucketlist(self):
        """Tests a bucketlist can be updated."""
        response = self.client.put('/api/bucket/1/', {'name': 'updated'},
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'detail': 'updated'})

    def test_duplicates_prevented_during_updates(self):
        """
        Tests error is raised when an updated bucketlist creates
        a duplicate.
        
        A bucket named 'testbucketlist' was already created in setUp.
        """
        response = self.client.put('/api/bucket/1/',
                                   {'name': 'testbucketlist'},
                                   format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_bucketlist(self):
        """Tests bucketlist deletion."""
        response = self.client.delete('/api/bucket/1/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'detail': 'deleted'})
