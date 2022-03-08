from rest_framework import filters, status, viewsets, mixins
from django.db.models import Exists, OuterRef
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.http.response import HttpResponse

from favs_N_shopping.models import Favorites, Purchase
from favs_N_shopping.serializers import FavoritesSerializer, PurchaseSerializer
from .models import Ingredient, Tag, Recipe, IngredientInRecipe
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer
from .paginators import RecipesCustomPagination
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrAdminOrReadOnly, IsOwnerOrReadOnly


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
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = RecipeSerializer
    pagination_class = RecipesCustomPagination
    lookup_url_kwarg = "id"
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user

        need_favorited = self.request.GET.get('is_favorited', False)
        need_in_shopping_cart = self.request.GET.get(
            'is_in_shopping_cart',
            False
        )
        if (
            user.is_anonymous
            or not (need_favorited or need_in_shopping_cart)
        ):
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
        # need_favorited = self.request.GET.get('is_favorited', False)
        # need_in_shopping_cart = self.request.GET.get(
        #     'is_in_shopping_cart',
        #     False
        # )
        if need_favorited and need_favorited != '0':
            need_favorited = True
        else:
            need_favorited = False
        if need_in_shopping_cart and need_in_shopping_cart != '0':
            need_in_shopping_cart = True
        else:
            need_in_shopping_cart = False

        # Касаемо префетч не уверен
        return queryset.filter(
            is_favorited=need_favorited,
            is_in_shopping_cart=need_in_shopping_cart
        ).select_related('author').prefetch_related('tags', 'ingredients')

    @action(
        detail=True, methods=['post', ],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, id=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)

        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        serializer = FavoritesSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # https://stackoverflow.com/questions/62084905/how-to-make-delete-method-in-django-extra-action
    @favorite.mapping.delete
    def delete_favorite(self, request, id=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        favorites = get_object_or_404(
            Favorites, user=user, recipe=recipe
        )
        favorites.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=['post', ],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, id=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)

        data = {
            'user': user.id,
            'recipe': recipe.id,
        }
        serializer = PurchaseSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, id=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        favorites = get_object_or_404(
            Purchase, user=user, recipe=recipe
        )
        favorites.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
