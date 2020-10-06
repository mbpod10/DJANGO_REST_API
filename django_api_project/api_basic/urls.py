from django.urls import path, include
from .views import article_list, article_detail, by_title
urlpatterns = [
    path('article/', article_list),
    path('detail/<int:pk>/', article_detail),
    path('title/<str:title>/', by_title)
]
