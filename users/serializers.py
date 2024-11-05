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
        fields = (
            'id',
            'email',
            'password',
            'phone',
            'city',
            'avatar',
            'is_active',
            'is_staff',
            'is_superuser',
            'payments',
        )


class UserCreateSerializer(ModelSerializer):
    """
    Сериализатор для регистрации пользователя
    """

    class Meta:
        model = User
        fields = ('email', 'password',)
