from rest_framework.serializers import ValidationError

# разрешенные ссылки на уроки
valid_video_urls = ['youtube.com', 'rutube.ru']


def validate_valid_video_url(value):
    """Проверка ссылки на разрешенные ресурсы"""
    for link in valid_video_urls:
        if link in value:
            return
    raise ValidationError('Ссылка на запрещенный ресурс')
