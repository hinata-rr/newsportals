from .views import (NewsListView, ArticlesListView, PostSearchView,
                   PostDetail, NewsCreate, ArticleCreate,
                   NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete)
from django.urls import path

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('search/', PostSearchView.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # Маршруты для статей
    path('articles/', ArticlesListView.as_view(), name='articles_list'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]