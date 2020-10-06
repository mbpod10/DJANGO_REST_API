from django.urls import path, include
# METHOD BASED
# from .views import article_list, article_detail, by_title

# CLASS BASED
from .views import ArticleDetails, ArticleAPIView

# GENERIC BASED
from .views import GenericAPIView

urlpatterns = [
    # path('article/', article_list),
    # path('detail/<int:pk>/', article_detail),
    path('detail/<int:id>/', ArticleDetails.as_view()),
    # path('title/<str:title>/', by_title)
    # path('article/', ArticleAPIView.as_view())
    path('article/', GenericAPIView.as_view()),
    path('article/<int:id>/', GenericAPIView.as_view())
]
