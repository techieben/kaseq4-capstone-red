from django.urls import path
from recipe import views

urlpatterns = [
    path('recipe/<int:id>/', views.RecipeView, name='recipe'),
    path('recipe_add/', views.RecipeAddView.as_view(), name='recipe_add'),
]
