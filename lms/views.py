from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.paginations import CustomPagination
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.models import Subs
from users.permissions import IsModer, IsOwner
from rest_framework.decorators import action
from lms.task import send_information_about_update_course


class CourseViewSet(ModelViewSet):
    """
    Контроллер для курса
    """

    queryset = Course.objects.all()
    pagination_class = CustomPagination

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

    def perform_update(self, serializer):
        """
        Рассылка оповещения об изменениях курса
        """
        course = serializer.save()
        email_list = []
        subs = Subs.objects.filter(course=course.pk)
        for sub in subs:
            email_list.append(sub.user.email)
        if email_list:
            message = f'Произведено обновление курса "{course.name}"'
            send_information_about_update_course.delay(email_list, message)


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

        # Рассылка оповещения о дополнении курса уроком
        email_list = []
        subs = Subs.objects.filter(course=lesson.course.pk)
        for sub in subs:
            email_list.append(sub.user.email)
        if email_list:
            message = f'К курсу "{lesson.course.name}" добавлен урок "{lesson.name}"'
            send_information_about_update_course.delay(email_list, message)


class LessonListAPIView(ListAPIView):
    """
    Контроллер для просмотра списка уроков
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagination


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

    def perform_update(self, serializer):
        """Рассылка оповещения об изменении урока в курсе"""
        lesson = serializer.save()
        email_list = []
        subs = Subs.objects.filter(course=lesson.course.pk)
        for sub in subs:
            email_list.append(sub.user.email)
        if email_list:
            message = f'У курса "{lesson.course.name}" изменен урок "{lesson.name}"'
            send_information_about_update_course.delay(email_list, message)


class LessonDestroyAPIView(DestroyAPIView):
    """
    Контроллер для удаления урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # удалять только владелец
    permission_classes = (IsOwner,)

    def perform_destroy(self, instance):
        """Рассылка оповещения об удалении урока в курсе"""
        email_list = []
        subs = Subs.objects.filter(course=instance.course_id)
        for sub in subs:
            email_list.append(sub.user.email)
        if email_list:
            message = f'У курса "{instance.course.name}" удален урок "{instance.name}"'
            send_information_about_update_course.delay(email_list, message)
        instance.delete()
