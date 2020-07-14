from django.urls import path
from recipe import views

urlpatterns = [
    path('recipe/<str:title>/', views.RecipeView, name='recipe'),
    path('recipe_add/', views.RecipeAddView.as_view(), name='recipe_add'),
    path('recipe_card/', views.RecipeCard, name='recipe_card'),
]

