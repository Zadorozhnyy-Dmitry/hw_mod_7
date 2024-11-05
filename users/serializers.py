from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для платежа
    """

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """
    Сериализатор для пользователя
    """
    payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = "__all__"
