import json
from rest_framework.test import APITestCase
from tests.test_base import BaseTestCase


class TestBucketlistViews(BaseTestCase):
    """
    Test bucketlist interactions.
    """
    def test_bucketlist_access_with_invalid_token(self):
        """Tests unauthorized error raised with invalid token."""
        self.client.force_authenticate(username=None)
        response = self.client.get('/bucketlists/')
        self.assertEqual(response.status_code, 401)

    def test_bucketlist_access_by_wrong_user(self):
        """
        Tests user cannot access bucketlists owned by another user.
    
        A test bucketlist created by a non-logged in user was
        created in setUp to test that user access works correctly.
        """
        response = self.client.get('/bucketlists/3')
        self.assertEqual(response.status_code, 404)
        self.assertIn(response.content, {'message': 'not found'})

    def test_create_bucketlist(self):
        """Tests a new bucketlist can be added."""
        response = self.client.post('/bucketlists/', {'title': 'bucketlist'},
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.data, {'title': 'Bucketlist'})

    def test_return_all_bucketlists(self):
        """Tests retrieval of all bucketlists."""
        response = self.client.get('/bucketlists/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_get_bucketlist(self):
        """
        Tests retrieval of a single bucketlist.

        Two test bucketlists were added in the setUp to
        test that the id parameter works correctly.
        """
        response = self.client.get('/bucketlists/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data, {'id': 2, 'title': 'testbucketlist2'})

    def test_update_bucketlist(self):
        """Tests a bucketlist can be updated."""
        response = self.client.put('/bucketlists/1', {'title': 'updated'},
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data, {'id': 1, 'title': 'updated'})

    def test_delete_bucketlist(self):
        """Tests bucketlist deletion."""
        response = self.client.delete('/bucketlists/1')
        self.assertEqual(response.status_code, 200)

    def test_results_limit(self):
        """Tests specified number of results retrieved from GET request."""
        response = self.client.get('/bucketlists/?limit=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(len(json.loads(response.context)), 1)

    def test_pagination(self):
        """Tests specified number of pages returned from GET request."""
        response = self.client.get('/bucketlists/?page=1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data, {'next': 'none'})

    def test_search_by_bucketlist_name(self):
        """Tests bucketlist can be retrieved from search."""
        response = self.client.get('/bucketlists/?q=Testbucketlist')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data, {'title': 'Testbucketlist'})

