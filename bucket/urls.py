from django.conf.urls import url

from bucket.views import (
    BucketlistAPIView,
    BucketlistDetailAPIView,
    ItemAPIView,
    ItemDetailAPIView
)

urlpatterns = [
    url(r'^$', BucketlistAPIView.as_view(), name='bucketlist'),
    url(r'^(?P<pk>[\d-]+)/$', BucketlistDetailAPIView.as_view(), name='bucketlist_detail'),
    url(r'^(?P<bucket>[\d-]+)/items/$', ItemAPIView.as_view(), name='item'),
    url(r'^(?P<bucket>[\d-]+)/items/(?P<pk>[\d-]+)/$', ItemDetailAPIView.as_view(), name='item_detail')
]
