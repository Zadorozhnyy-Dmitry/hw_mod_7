from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer

# Create your views here.


class UserViewSet(ModelViewSet):
    """
    Контроллер для пользователя
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


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
