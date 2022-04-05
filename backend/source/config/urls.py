from rest_framework.routers import DefaultRouter

from django.conf import settings
# from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from authentication.views import UpdatePassword
from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet

# from rest_framework_swagger.views import get_swagger_view

# from .import settings
# from django.contrib.staticfiles.urls import static

# schema_view = get_swagger_view(title='API docs')

router = DefaultRouter()
router.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredients'
)

router.register(
    r'tags',
    TagViewSet,
    basename='tags'
)

router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
    # re_path('api/swagger/', schema_view),
]

urlpatterns += [re_path('api/', include([
    path("users/set_password/", UpdatePassword.as_view(), name="set_password"),
    path('users/', include('users.urls'), name='users'),

    path('auth/', include('authentication.urls'), name='auth'),

    path('', include(router.urls)),
    ]))]

# Для дев режима с контейнерами
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
# Для дев режима с контейнерами
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
