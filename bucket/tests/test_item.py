from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from bucket.models import Item


class TestItemAPIView(APITestCase):
    """
    Test bucketlist item interactions.
    """
    def test_create_new_item(self):
        """Tests a new item can be added."""
        response = self.client.post('/api/bucket/1/items/', {'name': 'item'},
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {'detail': 'item'})
        # asserts that the item has been crated in the db
        self.assertTrue(Item.objects.filter(name='item'))

    def test_get_item(self):
        """
        Tests retrieval of a single item.
        Two test items were added in the setUp to
        test that the id parameter works correctly.
        """
        response = self.client.get('/api/bucket/1/items/2/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'detail': 'testitem2'})

    def test_update_bucketlist(self):
        """Tests a item can be updated."""
        response = self.client.put('/api/bucket/1/items/1/', {'name': 'updated'},
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'detail': 'updated'})

    def test_duplicates_prevented_during_updates(self):
        """
        Tests error is raised when an updated item creates
        a duplicate.
        
        An item named 'testitem' was already created in setUp.
        """
        response = self.client.put('/api/bucket/1/items/1/',
                                   {'name': 'testitem'},
                                   format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_bucketlist(self):
        """Tests item deletion."""
        response = self.client.delete('/api/bucket/1/items/1/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'detail': 'deleted'})
