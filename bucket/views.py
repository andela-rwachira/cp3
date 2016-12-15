from rest_framework import generics
from rest_framework.filters import SearchFilter

from bucket.models import Bucketlist, Item
from bucket.serializers import BucketlistSerializer, ItemSerializer
from bucket.utils import BucketlistPageNumberPagination


class BucketlistAPIView(generics.ListCreateAPIView):
    """
    Creates and lists all bucketlists.
    """
    serializer_class = BucketlistSerializer

    # enables keyword/id search and pagination
    filter_backends = [SearchFilter]
    search_fields = ('name', 'id')
    pagination_class = BucketlistPageNumberPagination

    def get_queryset(self):
        """Returns bucketlists created by current user."""
        queryset = Bucketlist.objects.filter(created_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Saves bucketlist with current user details."""
        serializer.save(created_by=self.request.user)


class BucketlistDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Updates and deletes specific bucketlists.
    """
    serializer_class = BucketlistSerializer

    def get_queryset(self):
        """Returns the bucketlist created by current user."""
        queryset = Bucketlist.objects.filter(created_by=self.request.user)
        return queryset


class ItemAPIView(generics.CreateAPIView):
    """
    Creates bucketlist items.
    """
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        """Saves item with current user and bucket."""
        queryset = Bucketlist.objects.filter(created_by=self.request.user)
        bucket_id = self.kwargs.get('bucket')
        bucketlist = queryset.get(id=bucket_id)
        serializer.save(created_by=self.request.user,
                        bucket=bucketlist)


class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Updates and deletes specific items.
    """
    serializer_class = ItemSerializer

    def get_queryset(self):
        """Returns the item created by current user in specific bucket."""
        queryset = Item.objects.filter(created_by=self.request.user)
        bucket = self.kwargs.get('bucket')
        item = self.kwargs.get('pk')
        return queryset.filter(bucket=bucket, id=item)
