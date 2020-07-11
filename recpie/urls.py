from django.urls import path
from recpie import views

urlpatterns = [
    path('', views.index, name="home"),
]