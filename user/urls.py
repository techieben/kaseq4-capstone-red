from django.contrib import admin
from django.urls import path, include
from allauth.account.views import LoginView, SignupView , LogoutView, EmailView


urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
]