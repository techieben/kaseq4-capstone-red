from django.urls import path, re_path
from recipe import views

urlpatterns = [
    path('recipe/<str:title>/', views.RecipeView.as_view(), name='recipe'),
    path('recipe_add/', views.RecipeAddView.as_view(), name='recipe_add'),
    path('recipe_edit/<str:title>/', views.RecipeEditView, name='recipe_edit'),
    path('favorite/<str:title>/', views.FavoriteView, name='favorite'),
    path('unfavorite/<str:title>/', views.UnfavoriteView, name='unfavorite'),
    re_path(r'^favorite_list/(?P<sort>\w+)/',
            views.FavoriteListView, name='favorite_list'),
    path('recipe_nutrition/<str:title>/', views.RecipeNutritionView, name='recipe_nutrition'),
    # path('contact_form/', views.ContactForm, name='contact_form'),
]
