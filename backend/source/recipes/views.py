from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Ingredient
from .serializers import IngredientSerialiser


@action(detail=True, methods=['LIST', ])
class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = IngredientSerialiser
    queryset = Ingredient.objects.all()
    filter_backends = (filters.SearchFilter,)
    pagination_class = None
    search_fields = ('^name',)
    ordering_fields = ('id',)
    lookup_url_kwarg = "id"
