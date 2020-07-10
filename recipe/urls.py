from django.urls import path
from recipe import views

urlpatterns = [
    path('recipe_detail/', views.recpie, name='recpie'),
]