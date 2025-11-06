from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from .models import Author, Category, PostCategory, Post, Comment, Subscription


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1
    verbose_name = "Категория"
    verbose_name_plural = "Категории"


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1
    verbose_name = "Подписка"
    verbose_name_plural = "Подписки"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content and title == content:
            raise ValidationError('Заголовок не должен совпадать с содержанием')

        return cleaned_data


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'rating', 'posts_count', 'comments_count')
    list_filter = ('rating',)
    search_fields = ('user__username', 'name')
    readonly_fields = ('rating',)

    def posts_count(self, obj):
        return obj.post_set.count()

    posts_count.short_description = 'Количество постов'

    def comments_count(self, obj):
        return Comment.objects.filter(user=obj.user).count()

    comments_count.short_description = 'Количество комментариев'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'posts_count', 'subscribers_count')
    list_filter = ('name',)
    search_fields = ('name',)
    inlines = [SubscriptionInline]

    def posts_count(self, obj):
        return obj.post_set.count()

    posts_count.short_description = 'Количество постов'

    def subscribers_count(self, obj):
        return obj.subscribers.count()

    subscribers_count.short_description = 'Подписчиков'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = (
        'title',
        'author',
        'post_type',
        'created_at',
        'rating',
        'categories_list',
        'comments_count',
        'preview_short'
    )
    list_filter = ('post_type', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__user__username')
    readonly_fields = ('created_at', 'rating')
    date_hierarchy = 'created_at'
    inlines = [PostCategoryInline]  # Убрали filter_horizontal, используем только inline

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'author', 'post_type')
        }),
        ('Дополнительно', {
            'fields': ('rating', 'created_at'),
            'classes': ('collapse',)
        }),
        # Убрали поле categories из fieldsets, т.к. оно управляется через inline
    )

    def categories_list(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    categories_list.short_description = 'Категории'

    def comments_count(self, obj):
        return obj.comment_set.count()

    comments_count.short_description = 'Комментарии'

    def preview_short(self, obj):
        return obj.preview()

    preview_short.short_description = 'Превью'

    actions = ['reset_rating', 'mark_as_news', 'mark_as_article']

    def reset_rating(self, request, queryset):
        updated = queryset.update(rating=0)
        self.message_user(request, f'Рейтинг сброшен для {updated} постов')

    reset_rating.short_description = 'Сбросить рейтинг'

    def mark_as_news(self, request, queryset):
        updated = queryset.update(post_type='NW')
        self.message_user(request, f'{updated} постов помечены как новости')

    mark_as_news.short_description = 'Пометить как новости'

    def mark_as_article(self, request, queryset):
        updated = queryset.update(post_type='AR')
        self.message_user(request, f'{updated} постов помечены как статьи')

    mark_as_article.short_description = 'Пометить как статьи'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'rating', 'content_short')
    list_filter = ('created_at', 'rating', 'user')
    search_fields = ('content', 'user__username', 'post__title')
    readonly_fields = ('created_at', 'rating')
    date_hierarchy = 'created_at'

    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_short.short_description = 'Комментарий'

    actions = ['reset_rating']

    def reset_rating(self, request, queryset):
        updated = queryset.update(rating=0)
        self.message_user(request, f'Рейтинг сброшен для {updated} комментариев')

    reset_rating.short_description = 'Сбросить рейтинг'


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    list_filter = ('category',)
    search_fields = ('post__title', 'category__name')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'subscribed_at')
    list_filter = ('subscribed_at', 'category')
    search_fields = ('user__username', 'category__name')
    readonly_fields = ('subscribed_at',)


# Кастомизация заголовков админ-панели
admin.site.site_header = "News Portal Administration"
admin.site.site_title = "News Portal Admin"
admin.site.index_title = "Добро пожаловать в панель управления News Portal"