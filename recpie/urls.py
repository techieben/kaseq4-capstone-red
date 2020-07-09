from django.urls import path
from recpie import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('add_recpie/', views.add_recpie, name='add_recpie'),
    path('add_author/', views.add_author, name='add_author'),
    path('author/<int:id>/', views.author, name='author'),
    path('recipe/<int:id>/', views.recpie, name='recpie'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('nutrition_label', views.nutrition_label, name='nutrition_label')
]