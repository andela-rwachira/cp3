"""bucketlist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import djoser.views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Bucket API')

urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),
    # User Auth
    url(r'^api/auth/login', obtain_jwt_token),  # using JSON web token
    url(r'^api/auth/register', djoser.views.RegistrationView.as_view()),
    # Bucket API
    url(r'^api/bucket/', include('bucket.urls')),
]

urlpatterns += [
    # Login button on the browsable API
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    # Swagger documentation
    url(r'^$', schema_view),
]
