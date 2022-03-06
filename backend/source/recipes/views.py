from rest_framework import filters, status, viewsets, mixins
from django.db.models import Exists, OuterRef
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly

from favs_N_shopping.models import Favorites, Purchase
from .models import Ingredient, Tag, Recipe, IngredientInRecipe
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer
from .paginators import RecipesCustomPagination
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrAdminOrReadOnly


# Переделать этот вьюсет, с использованием фильтрации
@action(detail=True)
class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filterset_class = IngredientFilter
    pagination_class = None
    ordering_fields = ('id',)
    lookup_url_kwarg = "id"

    # Костыльный метод фильтрации)
    # def get_queryset(self):
    #     queryset = Ingredient.objects.all()
    #     # Костыльно, но работает
    #     # Хотел сделать через SearchFilter, но по тз
    #     # нужно что бы name было квери параметром
    #     keywords = self.request.query_params.get('name')
    #     if keywords:
    #         queryset = queryset.filter(name__startswith=keywords)
    #     return queryset

# class IngredientViewSet(
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     permission_classes = (permissions.AllowAny,)
#     pagination_class = None
#     filter_backends = (DjangoFilterBackend,)
#     filter_class = IngredientFilter


@action(detail=True)
class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


@action(detail=True)
class RecipeViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrAdminOrReadOnly, ]
    serializer_class = RecipeSerializer
    pagination_class = RecipesCustomPagination
    # ordering_fields = ('id',)
    lookup_url_kwarg = "id"
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Recipe.objects.all()

        # Тут мы анотируем объекты рецепров полями is_favorited и
        # is_in_shopping_cart, в которых блягодаря Exists проставлены
        # True or False, опираясь на то, был ли id рецепта в таблице
        # Избранного / Покупок у user из реквеста
        queryset = Recipe.objects.annotate(
            # Что то новенькое...

            # OuterRef -
            # https://djangodoc.ru/3.2/ref/models/expressions/
            # #referencing-columns-from-the-outer-queryset

            # Exists -
            # https://djangodoc.ru/3.2/ref/models/expressions/
            # #exists-subqueries
            is_favorited=Exists(Favorites.objects.filter(
                user=user, recipe_id=OuterRef('pk')
            )),
            is_in_shopping_cart=Exists(Purchase.objects.filter(
                user=user, recipe_id=OuterRef('pk')
            ))
        )
        # if self.request.query_params.get('is_favorited'):
        if self.request.GET.get('is_favorited'):
            return queryset.filter(is_favorited=True)
        # if self.request.query_params.get('is_in_shopping_cart'):
        elif self.request.GET.get('is_in_shopping_cart'):
            return queryset.filter(is_in_shopping_cart=True)

        return queryset

