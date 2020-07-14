from django.urls import path
from recipe import views

urlpatterns = [
    path('recipe/<str:title>/', views.RecipeView.as_view(), name='recipe'),
    path('recipe_add/', views.RecipeAddView.as_view(), name='recipe_add'),
    path('favorite/<str:title>/', views.FavoriteView, name='favorite'),
    path('unfavorite/<str:title>/', views.UnfavoriteView, name='unfavorite'),
]
