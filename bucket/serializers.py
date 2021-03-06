from rest_framework import serializers
from bucket.models import Bucketlist, Item


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

    def validate_name(self, data):
        """Checks for duplicates."""
        user = self.context['request'].user
        queryset = Item.objects.filter(name__iexact=data, created_by=user)# case-insensitive name search
        if queryset.exists():
            raise serializers.ValidationError('This item already exists.')
        return data

    def get_created_by(self, obj):
        """Returns user name instead of user id."""
        return str(obj.created_by.username)

    def get_bucket(self, obj):
        """Returns bucketlist name instead of bucketlist id."""
        return str(obj.bucket.name)


class BucketlistSerializer(serializers.ModelSerializer):
    """
    Seralizes the Bucketlist model.
    """
    items = ItemSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created',
                  'date_modified', 'created_by', 'items')

    def validate(self, data):
        """Checks for duplicates."""
        user = self.context['request'].user
        name = data['name']
        queryset = Bucketlist.objects.filter(name__iexact=name, created_by=user)
        if queryset.exists():
            raise serializers.ValidationError('This bucketlist already exists.')
        return data

    def get_created_by(self, obj):
        """Returns user name instead of id number."""
        return str(obj.created_by.username)