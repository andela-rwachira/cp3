from bucket.models import Item
from test_base import BaseTestCase


class TestItemAPIView(BaseTestCase):
    """
    Test bucketlist item interactions.
    """

    def test_create_new_item(self):
        """Tests a new item can be added."""
        response = self.client.post('/api/bucket/1/items/', {'name': 'item'},
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
        response = self.client.post('/api/bucket/1/items/',
                                    {'name': 'an item'},
                                    format='json')
        self.assertEqual(response.status_code, 200)
        item = Item.objects.get(name='an item')
        self.assertTrue(item.done, False)

    def test_bucketlist_validation_for_new_item(self):
        """
        Tests error raised if bucketlist doesn't exist
        before creating a new item.
        """
        pass

    def test_invalid_name(self):
        """Tests error raised when empty string passed."""
        response = self.client.post('/api/bucket/1/items/', {'name': ''},
                                    format='json') 
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field may not be blank')

    def test_duplicates_prevented(self):
        """
        Tests error is raised for duplicates.
  
        An item named 'testitem' was already created in setUp.
        """
        response = self.client.post('/api/bucket/1/items/', {'name': 'testitem'},
                                    format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'This item already exists')

    def test_get_item(self):
        """
        Tests retrieval of a single item.
        Two test items were added in the setUp to
        test that the id parameter works correctly.
        """
        response = self.client.get('/api/bucket/1/items/2/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'testitem2')

    def test_invalid_item_get_request(self):
        """Tests error raised for an invalid get request."""
        response = self.client.get('/api/bucket/1/items/3', format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found')

    def test_invalid_update_request(self):
        """Tests error raised when requested item doesn't exist."""
        response = self.client.post('/bucketlists/1/items/3',
                                    {'name': 'update'},
                                    format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found')

    def test_update_name_field(self):
        """Tests name field can be updated."""
        response = self.client.put('/api/bucket/1/items/1/',
                                   {'name': 'updated'},
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updated')

    def test_invalid_name_update(self):
        """Tests error raised if empty string is passed."""
        response = self.client.put('/api/bucket/1/items/1/',
                                  {'name': ''}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['name'][0], 'This field may not be blank')

    def test_update_done_field(self):
        """Tests done field can be updated."""
        response = self.client.patch('/api/bucket/1/items/1/',
                                     {'done': 'True'},
                                     format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['done'], True) #or 'true'

    def test_invalid_done_update(self):
        """Tests error raised if empty string is passed."""
        response = self.client.patch('/api/bucket/1/items/1/',
                                     {'done': ''}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['done'][0], '"" is not a valid boolean') # or "\"\" is not a valid boolean."

    def test_duplicates_prevented_during_updates(self):
        """
        Tests error is raised when an updated item creates
        a duplicate.
        
        An item named 'testitem' was already created in setUp.
        """
        response = self.client.put('/api/bucket/1/items/2/',
                                   {'name': 'testitem'},
                                   format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'This item already exists')

    def test_delete_bucketlist(self):
        """Tests item deletion."""
        response = self.client.delete('/api/bucket/1/items/1/', format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Item.objects.filter(name='testitem'), None)

    def test_invalid_delete(self):
        """Tests error raised for an invalid delete request."""
        response = self.client.delete('/api/bucket/1/items/3/', format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found')
