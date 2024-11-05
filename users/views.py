from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, UserCreateSerializer


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
