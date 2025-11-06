from .views import (NewsListView, ArticlesListView, PostSearchView,
                   PostDetail, NewsCreate, ArticleCreate,
                   NewsUpdate, ArticleUpdate, NewsDelete, ArticleDelete, upgrade,
                    subscribe_to_category, unsubscribe_from_category)
from django.urls import path
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('news/', cache_page(60*5)(NewsListView.as_view()), name='news_list'),
    path('search/', cache_page(60)(PostSearchView.as_view()), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
    path('<int:pk>/update/', cache_page(5)(NewsUpdate.as_view()), name='news_update'),
    path('<int:pk>/delete/', cache_page(5)(NewsDelete.as_view()), name='news_delete'),

    # Маршруты для статей
    path('articles/', cache_page(60*5)(ArticlesListView.as_view()), name='articles_list'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/update/', cache_page(5)(ArticleUpdate.as_view()), name='article_update'),
    path('articles/<int:pk>/delete/', cache_page(5)(ArticleDelete.as_view()), name='article_delete'),

    path('upgrade/', upgrade, name = 'upgrade'),

    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_category'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe_from_category, name='unsubscribe_category'),
]