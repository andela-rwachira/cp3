from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bucketlist, Item


class UserSerializer(serializers.ModelSerializer):
    """
    Seralizes the User model.
    """
    bucketlists = serializers.HyperlinkedRelatedField(many=True,
                                                      read_only=True,
                                                      view_name='bucketlists')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'bucketlists')


class BucketlistSerializer(serializers.ModelSerializer):
    """
    Seralizes the Bucketlist model.
    """
    items = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name='items')

    class Meta:
        model = Bucketlist
        fields = ('id', 'name', 'date_created', 'date_modified', 'created_by', 'items')


class ItemSerializer(serializers.ModelSerializer):
    """
    Seralizes the Item model.
    """
    class Meta:
        model = Item
        fields = ('id', 'name', 'date_created', 'date_modified', 'created_by', 'bucket', 'done')
