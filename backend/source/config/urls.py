from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet

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
    path('users/', include('users.urls'), name='users'),

    path('auth/', include('djoser.urls.authtoken'), name='auth'),

    path('', include(router.urls)),
]))]

if settings.DEBUG:
    # Для дев режима с контейнерами
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
