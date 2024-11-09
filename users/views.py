from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from lms.models import Course
from users.models import Payment, User, Subs
from users.serializers import (PaymentSerializer, UserCreateSerializer,
                               UserSerializer, SubsSerializer)


class UserListAPIView(ListAPIView):
    """
    Контроллер просмотра пользователей
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Контроллер для регистрации пользователя
    """

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(ListAPIView):
    """
    Контроллер для просмотра списка платежей
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = (
        "course",
        "lesson",
        "method",
    )
    ordering_fields = ("paid_date",)


class PaymentCreateAPIView(CreateAPIView):
    """
    Контроллер для просмотра списка платежей
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class SubsAPIView(APIView):
    queryset = Subs.objects.all()
    serializer_class = SubsSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subs.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Вы отписались'
        else:
            Subs.objects.create(user=user, course=course_item)
            message = 'Вы подписались'
        return Response({"message": message})


class SubsListAPIView(ListAPIView):
    serializer_class = SubsSerializer
    queryset = Subs.objects.all()
