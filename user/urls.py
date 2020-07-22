from django.urls import path
from allauth.account.views import LoginView, SignupView, LogoutView
from user import views


urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),
    path('signup/', SignupView.as_view(), name='account_signup'),
    path('logout/', LogoutView.as_view(), name='account_logout'),
    path('profile/<str:username>/', views.ProfileView, name='profile'),
    path('profile_edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('follow/<str:username>/', views.FollowView, name='follow'),
    path('unfollow/<str:username>/', views.UnfollowView, name='unfollow'),
]
