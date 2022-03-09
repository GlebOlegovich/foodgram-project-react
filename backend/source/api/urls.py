from django.urls import include, path
# from django.conf.urls import url

from recipes.views import IngredientViewSet, TagViewSet, RecipeViewSet
from rest_framework.routers import DefaultRouter

from authentication.views import UpdatePassword

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
    path("users/set_password/", UpdatePassword.as_view(), name="set_password"),
    path('users/', include('users.urls'), name='users'),

    path('auth/', include('authentication.urls')),

    path('', include(router.urls)),

]
