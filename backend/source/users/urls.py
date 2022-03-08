from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SubscribeViewset, ListSubscriptions
# from .views import registration_user
from authentication.views import UpdatePassword

app_name = "users"


router = DefaultRouter()

router.register("", UserViewSet, basename="usersviewset")

urlpatterns = [
    path(
        "<int:author_id>/subscribe/",
        SubscribeViewset.as_view(),
        name="subscribe"
    ),
    path(
        "subscriptions/",
        ListSubscriptions.as_view(),
        name="list_subscriptions"
    ),
    path("", include(router.urls),),
]
