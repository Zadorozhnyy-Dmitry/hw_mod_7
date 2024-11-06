from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentListAPIView,
                         UserCreateAPIView, UserListAPIView)

app_name = UsersConfig.name

# # url for users
# router = SimpleRouter()
# router.register(
#     "",
#     UserViewSet,
# )

# urls for payments
urlpatterns = [
    path(
        "payments/", PaymentListAPIView.as_view(), name="payment-list"
    ),  # просмотр списка платежей
    path(
        "payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"
    ),  # создание платежа
    # эндпоинты для авторизации
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    # эндпоинты для пользователей
    path(
        "", UserListAPIView.as_view(), name="users-list"
    ),  # вывод списка пользователей
    path(
        "register/", UserCreateAPIView.as_view(), name="users-register"
    ),  # регистрация пользователя
]

# urlpatterns += router.urls
