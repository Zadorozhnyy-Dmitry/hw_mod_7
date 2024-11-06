from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.permissions import IsModer, IsOwner


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
        Права доступа
        """
        # модератор не может создавать курс
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        # изменить или детально просмотреть курс может или модератор, или владелец
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        # удалить курс может только владелец
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """
    Контроллер для создания урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # создавать урок может любой авторизированный пользователь кроме модератора
    permission_classes = (
        ~IsModer,
        IsAuthenticated,
    )

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
    # Детальный просмотр только модератор или владелец
    permission_classes = (IsModer | IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    """
    Контроллер для редактирования урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Изменять только модератор или владелец
    permission_classes = (IsModer | IsOwner,)


class LessonDestroyAPIView(DestroyAPIView):
    """
    Контроллер для удаления урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # удалять только владелец
    permission_classes = (IsOwner,)
