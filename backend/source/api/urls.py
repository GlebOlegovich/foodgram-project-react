from django.urls import include, path
# from django.conf.urls import url

from recipes.views import IngredientViewSet, TagViewSet, RecipeViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

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
    path('', include(router.urls)),
    path('users/', include('users.urls')),
    path('auth/', include('authentication.urls')),

]
