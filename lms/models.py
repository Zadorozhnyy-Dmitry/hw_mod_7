from django.db import models

from config.settings import NULLABLE


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Укажите описание курса", **NULLABLE
    )
    preview = models.ImageField(
        upload_to="lms/course_preview",
        verbose_name="Превью",
        help_text="Загрузите превью",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Урок", help_text="Укажите урок"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        **NULLABLE,
    )
    preview = models.ImageField(
        upload_to="lms/lesson_preview",
        verbose_name="Превью",
        help_text="Загрузите превью",
        **NULLABLE,
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
