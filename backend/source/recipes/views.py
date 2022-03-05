from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Ingredient, Tag
from .serializers import IngredientSerialiser, TagSerialiser


# Переделать этот вьюсет, с использованием фильтрации
@action(detail=True)
class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = IngredientSerialiser
    # queryset = Ingredient.objects.all()
    # filter_backends = (filters.SearchFilter, )
    # search_fields = ('^name',)
    pagination_class = None
    ordering_fields = ('id',)
    lookup_url_kwarg = "id"
    SEARCH_PARAM = 'name'

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        # Костыльно, но работает
        # Хотел сделать через SearchFilter, но по тз
        # нужно что бы name было квери параметром
        keywords = self.request.query_params.get('name')
        if keywords:
            queryset = queryset.filter(name__startswith=keywords)
        return queryset

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
    serializer_class = TagSerialiser
    queryset = Tag.objects.all()
