from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post
import time


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        time.sleep(0.1)

        instance.refresh_from_db()

    categories = instance.categories.all()
    print(f"🏷️  Категории: {[cat.name for cat in categories]}")

    if not categories:
        print("❌ Нет категорий - уведомления не отправляются")
        return

    print(f"🎯 СИГНАЛ: Новый пост '{instance.title}'")

    for category in categories:
        subscribers = category.subscribers.all()
        print(f"🔔 Категория '{category.name}': {subscribers.count()} подписчиков")

        if not subscribers:
            print(f"   ⚠️ Нет подписчиков в категории '{category.name}'")
            continue

        for user in subscribers:
            if user.email:
                print(f"   📧 Отправляем письмо для {user.username} ({user.email})")

                try:
                    html_content = render_to_string('account/email/new_post_notification.html', {
                        'post': instance,
                        'user': user,
                        'category': category,
                    })
                    msg = EmailMultiAlternatives(
                        subject=f'Новая запись в разделе "{category.name}"',
                        body=f'Здравствуй, {user.username}!\n\n'
                             f'В разделе "{category.name}" появилась новая запись:\n\n'
                             f'📰 {instance.title}\n'
                             f'📝 {instance.content[:100]}...\n\n'
                             f'➡️ Читать полностью: http://127.0.0.1:8000/news/{instance.id}/\n\n'
                             f'С уважением,\nКоманда News Portal',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    print(f"   ✅ Письмо отправлено на {user.email}")

                except Exception as e:
                    print(f"   ❌ Ошибка отправки: {e}")
            else:
                print(f"   ⚠️ У пользователя {user.username} нет email")

    print("✅ Все уведомления обработаны\n")