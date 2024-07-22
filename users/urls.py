from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateApiView, PaymentListApiView,
                         UserCreateApiView, UserListApiView)

app_name = UsersConfig.name
# Если работаем с PaymentViewSet
# from rest_framework.routers import SimpleRouter
# router = SimpleRouter()
# router.register("", PaymentViewSet, basename="course")
# urlpatterns += router.urls


urlpatterns = [
    path(
        "register/",
        UserCreateApiView.as_view(),
        name="register",
    ),
    path("", UserListApiView.as_view(), name="users"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("payments/", PaymentListApiView.as_view(), name="payments"),
    path("payment/create/", PaymentCreateApiView.as_view(), name="create_payment"),
]
