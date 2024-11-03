from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для курса
    """

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """
    Сериализатор для вывода информации о курсе с кол-вом уроков
    """

    count_lessons = SerializerMethodField()

    @staticmethod
    def get_count_lessons(course):
        return Lesson.objects.filter(course=course.pk).count()

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    """
    Сериализатор для урока
    """

    class Meta:
        model = Lesson
        fields = "__all__"
