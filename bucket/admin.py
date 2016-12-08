from django.contrib import admin
from .models import Bucketlist, Item

"""
Allows admins to create/update/delete
bucketlists and items from the admin dashboard.
"""
admin.site.register(Bucketlist)
admin.site.register(Item)
