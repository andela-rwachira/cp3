from rest_framework import serializers
from bucket.models import Bucketlist, Item


class BucketlistSerializer(serializers.ModelSerializer):
    """
    Seralizes the Bucketlist model.
    """
    items = serializers.StringRelatedField(many=True)
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created',
                  'date_modified', 'created_by', 'items')

    def get_created_by(self, obj):
        """Returns user name instead of id number."""
        return str(obj.created_by.username)


class ItemSerializer(serializers.ModelSerializer):
    """
    Seralizes the Item model.
    """
    created_by = serializers.SerializerMethodField()
    bucket = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('id', 'name', 'date_created',
                  'date_modified', 'created_by', 'bucket', 'done')

    def get_created_by(self, obj):
        """Returns user name instead of id number."""
        return str(obj.created_by.username)

    def get_bucket(self, obj):
        """Returns bucketlist name instead of id number."""
        return str(obj.bucket.name)
