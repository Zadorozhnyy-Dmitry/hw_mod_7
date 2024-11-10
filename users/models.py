from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE, AUTH_USER_MODEL
from lms.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35, verbose_name="Телефон", help_text="Укажите телефон", **NULLABLE
    )
    city = models.CharField(
        max_length=35, verbose_name="Город", help_text="Укажите город", **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите фото",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """
    Класс для платежей
    """

    METHOD_CHOICES = {("cash", "наличные"), ("transaction", "перевод")}
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь", **NULLABLE
    )
    paid_date = models.DateTimeField(
        default=datetime.now, verbose_name="Дата оплаты", **NULLABLE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Оплаченный курс", **NULLABLE
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name="Оплаченный урок", **NULLABLE
    )
    amount = models.PositiveSmallIntegerField(verbose_name="Сумма оплаты", **NULLABLE)
    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default="transaction",
        verbose_name="Метод платежа",
        **NULLABLE,
    )
    session_id = models.CharField(max_length=255, verbose_name='Id сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)

    def __str__(self):
        return f"{self.user} - оплатил за {self.course if self.course else self.lesson}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Subs(models.Model):
    """Модель для подписки"""
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)

    def __str__(self):
        return f'Пользователь {self.user} - подписан на {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
