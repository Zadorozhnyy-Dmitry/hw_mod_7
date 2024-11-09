from rest_framework.serializers import ModelSerializer, SerializerMethodField, URLField

from lms.models import Course, Lesson
from lms.validators import validate_valid_video_url
from users.models import Subs


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для курса
    """
    is_subs = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_subs(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subs.objects.filter(user=user, course=obj).exists()
        return False


class CourseDetailSerializer(ModelSerializer):
    """
    Сериализатор для вывода информации о курсе с кол-вом уроков
    """

    count_lessons = SerializerMethodField()
    lessons = SerializerMethodField()

    @staticmethod
    def get_count_lessons(course):
        return Lesson.objects.filter(course=course.pk).count()

    @staticmethod
    def get_lessons(course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """
    Сериализатор для урока
    """
    video_url = URLField(validators=[validate_valid_video_url])

    class Meta:
        model = Lesson
        fields = "__all__"
