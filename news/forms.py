from django import forms
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Post, Category, Author

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'content',
                  'author',
                  'categories',
        ]
    author = forms.ModelChoiceField(
        queryset=Author.objects.filter(user__is_staff=False),
        label='Автор',
        empty_label="Выберите автора",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(attrs={
            'placeholder': 'Заголовок статьи',
            'class': 'form-control title-input',
            'style': 'font-size: 14px; font-weight: bold;'
        })
    )

    content = forms.CharField(
        label='Содержание',
        widget=forms.Textarea(attrs={
            'placeholder': 'Ваш текст...',
            'class': 'form-control title-input',
            'style': 'font-size: 14px; font-weight: bold;'
        })
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        label='Категории',
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    post_type = forms.ChoiceField(
        choices=Post.POST_TYPES,
        label='Тип поста',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': 'font-size: 14px;'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        if content is not None and len(content) < 50:
            raise ValidationError({
                "description": "Описание не может быть менее 50 символов."
            })

        title = cleaned_data.get('title')
        if title == content:
            raise ValidationError(
                'Содержание не должно быть идентичным заголовку.'
            )

        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Заголовок должен начинаться с заглавной буквы."
            )
        return title

    def clean_content(self):
        content = self.cleaned_data["content"]
        if content[0].islower():
            raise ValidationError(
                "Содержание должно начинаться с заглавной буквы."
            )
        return content

class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


