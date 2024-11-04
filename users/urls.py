from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentCreateAPIView, PaymentListAPIView, UserViewSet

app_name = UsersConfig.name

# url for users
router = SimpleRouter()
router.register(
    "",
    UserViewSet,
)

# urls for payments
urlpatterns = [
    path(
        "payments/", PaymentListAPIView.as_view(), name="payment-list"
    ),  # просмотр списка платежей
    path(
        "payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"
    ),  # создание платежа
]

urlpatterns += router.urls
