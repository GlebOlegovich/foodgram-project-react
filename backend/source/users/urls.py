from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, Subscribe
# from .views import registration_user
from auth.views import UpdatePassword

app_name = "users"


router = DefaultRouter()

router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("set_password/", UpdatePassword.as_view(), name="set_password"),
    path("", include(router.urls)),
    path("<int:author_id>/subscribe/", Subscribe.as_view(), name="subscribe")
]
