from rest_framework.pagination import PageNumberPagination


class BucketlistPageNumberPagination(PageNumberPagination):
    """Overrides the default pagination settings."""
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 100
