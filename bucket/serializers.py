from rest_framework import serializers
from bucket.models import Bucketlist, Item


class BucketlistSerializer(serializers.ModelSerializer):
    """
    Seralizes the Bucketlist model.
    """
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created',
                  'date_modified', 'created_by', 'items')


class ItemSerializer(serializers.ModelSerializer):
    """
    Seralizes the Item model.
    """
    class Meta:
        model = Item
        fields = ('id', 'name', 'date_created',
                  'date_modified', 'created_by', 'bucket', 'done')
