from datetime import timedelta

from django.core.mail import send_mail

from celery import shared_task

from config.settings import EMAIL_HOST_USER
from django.utils import timezone

from users.models import User


@shared_task
def send_information_about_update_course(email_list, message):
    """Рассылка информации об обновлении материалов курса"""
    send_mail(
        subject="Обновление курса",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=email_list,
    )


@shared_task
def deactivate_users():
    """Блокировка пользователя если он не заходил более месяца"""
    today = timezone.now()
    users = User.objects.all()
    for user in users:
        if user.last_login:
            delta_last_login = today - user.last_login
            if delta_last_login < timedelta(days=30):
                continue
        else:
            user.is_active = False
            user.save()
