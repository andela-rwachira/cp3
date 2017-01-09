from bucket.models import Item
from .test_base import BaseTestCase


class TestItemAPIView(BaseTestCase):
    """
    Test bucketlist item interactions.
    """

    def test_unauthorized_access(self):
        """Tests error raised when user is not authorised."""
        self.client.credentials()
        response = self.client.post('/api/bucket/{}/items/'.format(self.bucketlist.id),
                                    {'name': 'item'},
                                    format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_create_new_item(self):
        """Tests a new item can be added."""
        response = self.client.post('/api/bucket/{}/items/'.format(self.bucketlist.id),
                                    {'name': 'item'},
                                    format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'item')

        # asserts that the item has been crated in the db
        self.assertTrue(Item.objects.filter(name='testitem'))

    def test_done_defaults_to_false(self):
        """
        Tests done field defaults to False
        for new items.
        """
        response = self.client.post('/api/bucket/{}/items/'.format(self.bucketlist.id),
                                    {'name': 'another item'},
                                    format='json')
        self.assertEqual(response.status_code, 201)
        item = Item.objects.filter(name='another item')
        self.assertFalse(item[0].done)

    def test_bucketlist_validation_for_new_item(self):
        """
        Tests error raised if bucketlist doesn't exist
        before creating a new item.
        """
        response = self.client.post('/api/bucket/3/items/',
                                    {'name': 'item'},
                                    format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_invalid_name(self):
        """Tests error raised when empty string passed."""
        response = self.client.post('/api/bucket/{}/items/'.format(self.bucketlist.id),
                                    {'name': ''},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')

    def test_duplicates_prevented(self):
        """
        Tests error is raised for duplicates.
  
        An item named 'testitem' was already created in setUp.
        """
        response = self.client.post('/api/bucket/{}/items/'.format(self.bucketlist.id),
                                    {'name': 'testitem'},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This item already exists.')

    def test_get_item(self):
        """
        Tests retrieval of a single item.
        Two test items were added in the setUp to
        test that the id parameter works correctly.
        """
        response = self.client.get(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, self.item2.id), format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'testitem2')

    def test_invalid_item_get_request(self):
        """Tests error raised for an invalid get request."""
        response = self.client.get(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, 3), format='json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_invalid_update_request(self):
        """Tests error raised when requested item doesn't exist."""
        response = self.client.get(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, 3), format='json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_update_name_field(self):
        """Tests name field can be updated."""
        response = self.client.put(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, self.item.id),
                {'name': 'updated'}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updated')

    def test_invalid_name_update(self):
        """Tests error raised if empty string is passed."""
        response = self.client.put(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, self.item.id),
                {'name': ''}, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field may not be blank.')

    def test_update_done_field(self):
        """Tests done field can be updated."""
        response = self.client.patch(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, self.item.id),
                {'done': 'true'}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['done'], True)

    def test_invalid_done_update(self):
        """Tests error raised if empty string is passed."""
        response = self.client.patch(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, self.item.id),
                {'done': ''}, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['done'][0], '"" is not a valid boolean.')

    def test_duplicates_prevented_during_updates(self):
        """
        Tests error is raised when an updated item creates
        a duplicate.

        An item named 'testitem' was already created in setUp.
        """
        response = self.client.put(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, self.item.id),
                {'name': 'testitem'}, format='json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This item already exists.')

    def test_delete_bucketlist(self):
        """Tests item deletion."""
        response = self.client.delete(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, self.item.id), format='json'
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Item.objects.filter(name='testitem').count(), 0)

    def test_invalid_delete(self):
        """Tests error raised for an invalid delete request."""
        response = self.client.delete(
            '/api/bucket/{0}/items/{1}/'.format(
                self.bucketlist.id, 3), format='json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')
