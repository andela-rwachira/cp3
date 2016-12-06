from rest_framework.test import APITestCase
from tests.test_base import BaseTestCase


class TestBucketItemViews(BaseTestCase):
    """
    Test bucketlist item interactions.
    """
    item_data = {'title': 'item', 'done': ''}
    client.force_authenticate(user=self.user)

    def test_endpoint_access_with_invalid_token(self):
        """Tests unauthorized error raised with invalid token."""
        response = self.client.post('/bucketlists/1/items/', self.item_data,
                                    format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_bucketlist(self):
        """Tests a new bucketlist can be added."""
        response = self.client.post('/bucketlists/1/items/', self.item_data,
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(response.data, {'title': 'item'})
        # asserts that the bucketlist item is assigned to the correct bucketlist
        item = BucketlistItem.objects.get(title='item')
        self.assertEqual(item.bucket, 1)

    def test_bucketlist_validation_for_new_item(self):
        """
        Tests error raised if bucketlist doesn't exist
        before creating a new item.
        """
        response = self.client.post('/bucketlists/3/items/', self.item_data,
                                    format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn(response.content, {'message': 'not found'})

    def test_invalid_name(self):
        """Tests error raised when empty string passed."""
        response = self.client.post('/bucketlists/1/items/',
                                    {'title': '', 'done': ''},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.data, {'message': 'must have a name'})

    def test_done_defaults_to_false(self):
        """
        Tests for new items, when the done field is
        an empty string, it defaults to False in the db.
        """
        response = self.client.post('/bucketlists/1/items/', self.item_data,
                                    format='json')
        self.assertEqual(response.status_code, 201)
        item = BucketlistItem.objects.get(title='item')
        self.assertTrue(item.done, False)

    def test_item_duplicates_prevented(self):
        """
        Tests error is raised for item duplicates.

        An item named 'testitem' was already created in test_base.
        """
        response = self.client.post('/bucketlists/1/items/',
                                    {'title': 'testitem', 'done': ''},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.content, {'message': 'already exists'})

    def test_invalid_update_request(self):
        """Tests error raised when requested item doesn't exist."""
        response = self.client.post('/bucketlists/1/items/2',
                                    {'title': 'update'},
                                    format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn(response.content, {'message': 'not found'})

    def test_update_name_field(self):
        """Tests an item's name can be updated."""
        response = self.client.put('/bucketlists/1/items/1',
                                   {'title': 'updated'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.data, {'title': 'updated'})

    def test_invalid_name_update(self):
        """Tests name is not changed even if empty string is passed."""
        response = self.client.put('/bucketlists/1/items/1',
                                  {'title': ''}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BucketlistItem.objects.get().title, 'testitem')

    def test_update_item_done_field(self):
        """Tests an item's done field can be updated."""
        response = self.client.put('/bucketlists/1/items/1',
                                   {'done': 'yes'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(BucketlistItem.objects.get().done, True)

    def test_invalid_done_update(self):
        """Tests done is not changed even if empty string is passed."""
        response = self.client.put('/bucketlists/1/items/1',
                                   {'done': ''}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(BucketlistItem.objects.get().done, False)

    def test_delete_item(self):
        """Tests an item can be deleted."""
        response = self.client.delete('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 200)
        # asserts that the item has been deleted from the db
        self.assertEqual(BucketlistItem.objects.get(id=1), None)

    def test_invalid_delete(self):
        """Tests error raised for an invalid delete request."""
        response = self.client.delete('/bucketlists/1/items/2')
        self.assertEqual(response.status_code, 404)
        self.assertIn(response.content, {'message': 'not found'})
