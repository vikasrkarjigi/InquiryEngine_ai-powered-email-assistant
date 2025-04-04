"""
URL configuration for email_auto_reply_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views, model_util

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('api/auto_reply_email', views.auto_reply_email, name='auto_reply_email'), #New API endpoint
    path('api/get_inquiry_history/', model_util.get_inquiry_history, name = 'get_inquiry_history')
]
