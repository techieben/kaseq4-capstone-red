from django.urls import path, re_path
from recipe import views

urlpatterns = [
    path('recipe/<str:title>/', views.RecipeView.as_view(), name='recipe'),
    path('recipe_add/', views.RecipeAddView.as_view(), name='recipe_add'),
    path('favorite/<str:title>/', views.FavoriteView, name='favorite'),
    path('unfavorite/<str:title>/', views.UnfavoriteView, name='unfavorite'),
    # path('favorite_list/', views.FavoriteListView, name='favorite_list'),
    re_path(r'^favorite_list/(?P<sort>\w+)/',
            views.FavoriteListView, name='favorite_list'),
    path('recipe_card/', views.RecipeCard, name='recipe_card'),
]
