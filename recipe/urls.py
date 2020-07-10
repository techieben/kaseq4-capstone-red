from django.urls import path
from recipe import views

urlpatterns = [
    path('recipe_all/', views.recpie, name='recpie'),
]