from django_filters import CharFilter
from django_filters.rest_framework import FilterSet, filters

from django.contrib.auth import get_user_model
from django.db.models import Case, IntegerField, Q, When

from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientFilter(FilterSet):
    # а тут мы говорим что для такого квери параметра name =
    # у нас для фильртации должны использоваться значения из поля
    # модели field_name="name"  а сама логика описывается в методе
    # method="name_filter"
    name = CharFilter(field_name="name", method="name_filter")

    class Meta:
        model = Ingredient
        # Квери параметр
        fields = ["name"]

    # **В качестве усложнения** можно сделать двойную фильтрацию:
    #     - по вхождению в начало названия;
    #     - по вхождению в произвольном месте.
    @staticmethod
    def name_filter(queryset, name, value):
        return (
            queryset.filter(**{f"{name}__icontains": value})
            .annotate(
                order=Case(
                    When(
                        Q(**{f"{name}__istartswith": value}),
                        then=1,
                    ),
                    When(
                        Q(**{f"{name}__icontains": value})
                        & ~Q(**{f"{name}__istartswith": value}),
                        then=2,
                    ),
                    output_field=IntegerField(),
                )
            )
            .order_by("order")
        )


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    # ForeignKey by default
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    # Альтернативный вариант сортировки, вместо сортировки в кверисете
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    def filter_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(purchases__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
