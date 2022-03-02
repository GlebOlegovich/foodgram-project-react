from django.urls import include, path

app_name = "api"

urlpatterns = [
    # path("v1/auth/", include(
    #     [
    #         path("signup/", get_or_create_user, name="get_or_create_user"),
    #         path("token/", get_token, name="get_token"),
    #     ]
    # )),
    path("users", include("api.users.urls", namespace="users")),
    # path("auth", include("auth.urls", namespace="auth")),
]
