from django.core.mail import send_mail

from celery import shared_task

from config.settings import EMAIL_HOST_USER


@shared_task
def send_information_about_update_course(email, message):
    """Рассылка информации об обновлении материалов курса"""
    send_mail(
        subject="Обновление курса",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
    )

    # print(f'{email} : {message}')
