from django.urls import path
from review import views

urlpatterns = [
    path('review_like/<int:id>/', views.UpvoteView, name='review_like'),
    path('review_unlike/<int:id>/', views.DownvoteView, name='review_unlike'),
    path('review_edit/<int:id>/', views.ReviewEditView.as_view(), name='review_edit'),
]
