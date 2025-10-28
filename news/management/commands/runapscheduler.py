import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
try:
    from news.models import Category, Post
except ImportError:
    from ..models import Category, Post

logger = logging.getLogger(__name__)


def send_weekly_digest():
    print("📧 Запуск еженедельной рассылки...")

    week_ago = timezone.now() - timedelta(days=7)
    total_emails = 0

    for category in Category.objects.all():
        new_posts = Post.objects.filter(
            categories=category,
            created_at__gte=week_ago
        ).order_by('-created_at')

        if not new_posts:
            continue

        subscribers = category.subscribers.all()

        for user in subscribers:
            if user.email:
                try:
                    html_content = render_to_string('account/email/weekly_digest.html', {
                        'user': user,
                        'category': category,
                        'posts': new_posts,
                        'week_ago': week_ago,
                    })

                    msg = EmailMultiAlternatives(
                        subject=f'📰 Еженедельная рассылка: {new_posts.count()} новых статей в разделе "{category.name}"',
                        body=f'Здравствуй, {user.username}!\n\n'
                             f'За неделю в разделе "{category.name}" появилось {new_posts.count()} новых статей.\n\n'
                             f'Читайте на нашем портале: http://127.0.0.1:8000/news/\n\n'
                             f'С уважением,\nNews Portal',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    total_emails += 1
                    print(f"   ✅ Отправлено {user.email}")

                except Exception as e:
                    print(f"   ❌ Ошибка: {e}")

    print(f"✅ Рассылка завершена. Отправлено писем: {total_emails}")


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_weekly_digest,
            trigger=CronTrigger(day_of_week=0, hour=9, minute=0),
            id="weekly_digest",
            max_instances=1,
            replace_existing=True,
        )
        print("✅ Добавлена еженедельная рассылка (воскресенье 9:00)")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        print("✅ Добавлена очистка старых задач")

        try:
            print("🚀 Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            print("🛑 Остановка...")
            scheduler.shutdown()