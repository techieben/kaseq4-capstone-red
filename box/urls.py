"""box URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from . import views

from recipe.urls import urlpatterns as recipe_urls
from user.urls import urlpatterns as user_urls
from review.urls import urlpatterns as review_urls
from notification.urls import urlpatterns as notification_urls
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', views.IndexView, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += recipe_urls + user_urls + review_urls + notification_urls


handler500 = 'recipe.views.error_500'
handler404 = 'recipe.views.error_404'
