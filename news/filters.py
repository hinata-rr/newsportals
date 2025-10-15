from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from django import forms
from .models import Post, Category, Author


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по заголовку',
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    category = ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    class Meta:
        model = Post
        fields = []

class PostSearchFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите часть названия...',
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Все авторы',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    created_after = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Опубликовано после',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    post_type = CharFilter(
        field_name='post_type',
        lookup_expr='exact',
        label='Тип записи',
        widget=forms.Select(choices=[('', 'Все типы')] + Post.POST_TYPES, attrs={
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created_after', 'post_type']