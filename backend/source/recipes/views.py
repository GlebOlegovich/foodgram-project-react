import itertools
import os

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django.http.response import HttpResponse

from config.settings import BASE_DIR
from favs_n_shopping.models import Favorite, Purchase
from favs_n_shopping.serializers import FavoriteSerializer, PurchaseSerializer

from .filters import IngredientFilter, RecipeFilter
from .mixins import AddOrDeleteRecipeFromFavOrShoppingModelMixin
from .models import Ingredient, Recipe, Tag
from .paginators import RecipesCustomPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, TagSerializer)

User = get_user_model()

# https://old.fonts-online.ru/font/Bee-Three - шрифт отсюда брал
FONT_PATH = os.path.join(os.path.join(BASE_DIR, 'templates'), '19207.ttf')


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
                    AddOrDeleteRecipeFromFavOrShoppingModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsOwnerOrReadOnly, ]
    # serializer_class = RecipeSerializer
    pagination_class = RecipesCustomPagination
    lookup_url_kwarg = "id"
    queryset = Recipe.objects.all()
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
        return RecipeCreateSerializer

    # !!!!!!!!!!!!
    # НЕ юзаем, вместо этого фильтрация в фильтрах
    # !!!!!!!!!!!!
    def _get_queryset_filtered_by_favorited_and_shopping_cart(self):
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
            is_favorited=Exists(Favorite.objects.filter(
                user=user, recipe_id=OuterRef('pk')
            )),
            is_in_shopping_cart=Exists(Purchase.objects.filter(
                user=user, recipe_id=OuterRef('pk')
            ))
        )

        if need_favorited and need_favorited != '0':
            return queryset.filter(
                is_favorited=True
            ).select_related('author').prefetch_related('tags', 'ingredients')

        if need_in_shopping_cart and need_in_shopping_cart != '0':
            return queryset.filter(
                is_in_shopping_cart=True
            ).select_related('author').prefetch_related('tags', 'ingredients')

        # Касаемо префетч не уверен
        return queryset.select_related('author').prefetch_related(
            'tags', 'ingredients'
        )

    @action(
        detail=True, methods=['post', ],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, id=None):
        return self.adding_recipe_to_model_with_serializer(
            request=request,
            root_serializer=FavoriteSerializer,
            recipe_id=id
        )

    # https://stackoverflow.com/questions/62084905/
    # how-to-make-delete-method-in-django-extra-action
    @favorite.mapping.delete
    def delete_favorite(self, request, id=None):
        return self.delete_recipe_from_model(
            model=Favorite,
            request=request,
            recipe_id=id
        )

    @action(
        detail=True, methods=['post', ],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, id=None):
        return self.adding_recipe_to_model_with_serializer(
            request=request,
            root_serializer=PurchaseSerializer,
            recipe_id=id
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, id=None):
        return self.delete_recipe_from_model(
            model=Purchase,
            request=request,
            recipe_id=id
        )

    # !!!!!!!!!!!!
    # НЕ юзаем, пытался сделать через xhtm2pdf, мб еще допилю...
    # !!!!!!!!!!!!

    # Пытался выполнить все через xhtml2pdf...
    # PDF из шаблона делается, но вместо кириллицы - квадраты...
    # @action(
    #     detail=False, methods=['get', ],
    #     # permission_classes=[IsAuthenticated])
    #     permission_classes=[AllowAny])
    # def download_shopping_cart(self, request):
    #     user = User.objects.get(id=1)
    #     # shopping_list = request.user._get_user_shopping_cart
    #     shopping_list = user._get_user_shopping_cart
    #     # for item in shopping_list['purchases']:
    #     #     print(shopping_list['purchases'][item])
    #     # shopping_list = []
    #     # for item in list:
    #     #     shopping_list.append(f'{item} - {list[item]["amount"]} '
    #     #                          f'{list[item]["measurement_unit"]} \n')
    #    response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    #     # response['Content-Disposition'] = (
    #     #     'attachment; filename="shoplist.txt"'
    #     # )

    #     # return response
    #     return render_pdf_view(shopping_list)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        shopping_list = request.user._get_user_shopping_cart()

        if shopping_list is None:
            error = {'errors': 'Список рецептов пуст'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        recipes = [recipe for recipe in shopping_list['recipes_in_cart']]
        purchases = shopping_list['purchases']
        response = HttpResponse(
            content_type='application/pdf'
        )
        response['Content-Disposition'] = (
            'attachment; '
            'filename="shopping_cart.pdf"'
        )
        canvas = Canvas(response)

        pdfmetrics.registerFont(TTFont('FontPDF', FONT_PATH))
        canvas.setFont('FontPDF', 50)
        canvas.drawString(
            100, 750,
            "Список покупок, для рецептов:"
        )
        canvas.setFont('FontPDF', 30)
        canvas.drawString(
            100, 700,
            f"{', '.join(recipes)}"
        )
        canvas.setFont('FontPDF', 30)
        counter = itertools.count(650, -50)
        for item in purchases:

            height = next(counter)
            canvas.drawString(
                50, height,
                f"-  {item['ingredient_name']} "
                f"- {item['ingredient_amount']}"
                f"{item['ingredient_measurement_unit']}"
            )
        canvas.save()

        request.user._clean_up_shopping_cart()

        return response
