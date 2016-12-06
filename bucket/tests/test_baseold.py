from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):
    """
    A base test case which creates dummy
    user, bucketlist and bucketlist item db entries.
    """
    def setUp(self):
        # create test user
        self.user = User.objects.create(username='testuser', password='pass')
        self.user2 = User.objects.create(username='testuser2', password='pass2')
        self.client.force_authenticate(user=self.user)

        # create test bucketlist items
        self.test_bucket = Bucketlist.objects.create(title='testbucketlist',
                                                     created_by=self.user.id)
        self.test_bucket2 = Bucketlist.objects.create(title='testbucketlist2',
                                                      created_by=self.user.id)
        self.test_bucket3 = Bucketlist.objects.create(title='testbucketlist3',
                                                      created_by=self.user2.id)
        # create test item
        self.test_item = BucketlistItem.objects.create(title='testitem',
                                                       done='',
                                                       bucket=self.test_bucket.id,
                                                       created_by=self.user.id)

    def tearDown(self):
        del self.user
        del self.test_bucket
        del self.test_bucket2
        del self.test_bucket3
        del self.test_item
