from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Удаляет все статьи в указанной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        Post = apps.get_model('news', 'Post')
        Category = apps.get_model('news', 'Category')
        PostCategory = apps.get_model('news', 'PostCategory')  # если есть промежуточная модель

        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no: ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = Category.objects.get(name=options['category'])
            # Находим посты через промежуточную модель
            post_ids = PostCategory.objects.filter(category=category).values_list('post_id', flat=True)
            posts_count = len(post_ids)
            Post.objects.filter(id__in=post_ids).delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно удалено {posts_count} статей из категории {category.name}'
                )
            )
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Не найдена категория {options["category"]}')
            )