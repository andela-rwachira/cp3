from bucket.models import Bucketlist
from test_base import BaseTestCase


class TestBucketlistAPIView(BaseTestCase):
    """
    Test bucketlist interactions.
    """

    def test_unauthorized_access(self):
        """Tests error raised when user is not authorised."""
        self.client.credentials()
        response = self.client.post('/api/bucket/', {'name': 'bucket'},
                                    format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_create_new_bucketlist(self):
        """Tests a new bucketlist can be added."""
        response = self.client.post('/api/bucket/', {'name': 'bucketlist'},
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'bucketlist')

        # asserts that the bucketlist has been crated in the db
        self.assertTrue(Bucketlist.objects.filter(name='bucketlist'))

    def test_invalid_name(self):
        """Tests error raised when empty string passed."""
        response = self.client.post('/api/bucket/', {'name': ''},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')

    def test_duplicates_prevented(self):
        """
        Tests error is raised for duplicates.
  
        A bucket named 'testbucketlist' was already created in setUp.
        """
        response = self.client.post('/api/bucket/', {'name': 'testbucketlist'},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'This bucketlist already exists.')   

    def test_return_all_bucketlists(self):
        """Tests retrieval of all bucketlists."""
        response = self.client.get('/api/bucket/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], Bucketlist.objects.count())

    def test_get_bucketlist(self):
        """
        Tests retrieval of a single bucketlist.
        Two test bucketlists were added in the setUp to
        test that the id parameter works correctly.
        """
        response = self.client.get('/api/bucket/{}/'.format(self.bucketlist2.id), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'testbucketlist2')

    def test_invalid_bucketlist_get_request(self):
        """Tests error raised for an invalid get request."""
        response = self.client.get('/api/bucket/3/', format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_update_bucketlist(self):
        """Tests a bucketlist can be updated."""
        response = self.client.put('/api/bucket/{}/'.format(self.bucketlist.id), {'name': 'updated'},
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updated')

    def test_invalid_update_request(self):
        """Tests error raised when requested item doesn't exist."""
        response = self.client.put('/api/bucket/3/', {'name': 'updated'},
                                   format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_duplicates_prevented_during_updates(self):
        """
        Tests error is raised when an updated bucketlist creates
        a duplicate.

        A bucket named 'testbucketlist' was already created in setUp.
        """
        response = self.client.put('/api/bucket/{}/'.format(self.bucketlist.id),
                                   {'name': 'testbucketlist'},
                                   format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'This bucketlist already exists.')

    def test_delete_bucketlist(self):
        """Tests bucketlist deletion."""
        response = self.client.delete('/api/bucket/{}/'.format(self.bucketlist.id), format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Bucketlist.objects.filter(name='testbucketlist').count(), 0)

    def test_invalid_delete(self):
        """Tests error raised for an invalid delete request."""
        response = self.client.delete('/api/bucket/3/', format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_results_limit(self):
        """Tests specified number of results retrieved from GET request."""
        response = self.client.get('/api/bucket/?limit=1', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['next'])

    def test_pagination(self):
        """Tests specified number of pages returned from GET request."""
        response = self.client.get('/api/bucket/?page=1', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['next'], None)

    def test_search_by_bucketlist_name(self):
        """Tests bucketlist can be retrieved from search."""
        response = self.client.get('/api/bucket/?search=testbucketlist')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['results'][0]['name'], 'testbucketlist')
