from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


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


class PaymentCreateAPIView(CreateAPIView):
    """
    Контроллер для просмотра списка платежей
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
