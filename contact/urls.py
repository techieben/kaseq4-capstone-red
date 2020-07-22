from django.urls import path
from contact import views

urlpatterns = [
    path('contact_us/', views.AddContactView, name='contact'),
]
