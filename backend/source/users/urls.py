from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (ListSubscriptions, SubscribeViewset, UpdatePassword,
                    UserViewSet)

app_name = "users"


router = DefaultRouter()

router.register("", UserViewSet, basename="usersviewset")

urlpatterns = [
    path(
        "set_password/",
        UpdatePassword.as_view(),
        name="set_password"
    ),
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
