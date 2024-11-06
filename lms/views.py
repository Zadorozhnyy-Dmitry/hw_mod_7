from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.permissions import IsModer


class CourseViewSet(ModelViewSet):
    """
    Контроллер для курса
    """

    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """
        Автоматическая запись пользователя в атрибут owner
        """
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """
        Права доступа для модератора
        :return:
        """
        # запрет модератору создавать и удалять курс
        if self.action in ['create', 'destroy', ]:
            self.permission_classes = (~IsModer,)
        # разрешение модератору редактировать и просматривать курс
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """
    Контроллер для создания урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # запрет модератору создавать урок
    permission_classes = [~IsModer,]

    def perform_create(self, serializer):
        """
        Автоматическая запись пользователя в атрибут owner
        """
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """
    Контроллер для просмотра списка уроков
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер для просмотра одного урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(UpdateAPIView):
    """
    Контроллер для редактирования урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    """
    Контроллер для удаления урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # запрет модератору удалять урок
    permission_classes = [~IsModer,]
