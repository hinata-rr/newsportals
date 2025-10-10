from .views import NewsListView, NewDetail
from django.urls import path

urlpatterns = [
    path('', NewsListView.as_view()),
    path('<int:pk>', NewDetail.as_view()),
]