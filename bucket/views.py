# from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import Bucketlist, Item
from .serializers import BucketlistSerializer, ItemSerializer


class BucketlistAPIView(generics.ListCreateAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BucketlistDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bucketlist.objects.all()
    serializer_class = BucketlistSerializer


class ItemAPIView(generics.CreateAPIView):
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        queryset = Bucketlist.objects.all()
        bucket_id = self.kwargs.get('bucket')
        bucketlist = queryset.get(id=bucket_id)
        serializer.save(created_by=self.request.user,
                        bucket=bucketlist)


class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        bucket = self.kwargs.get('bucket')
        item = self.kwargs.get('pk')
        return queryset.filter(bucket=bucket, id=item)
