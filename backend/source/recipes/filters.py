import django_filters as filters
from django.db.models import Case, IntegerField, Q, When
from django_filters import CharFilter

from recipes.models import Ingredient, Recipe


class IngredientFilter(filters.FilterSet):
    # а тут мы говорим что для такого квери параметра name =
    # у нас для фильртации должны использоваться значения из поля
    # модели field_name="name"  а сама логика описывается в методе
    # method="name_filter"
    name = CharFilter(field_name="name", method="name_filter")

    class Meta:
        model = Ingredient
        # Квери параметр
        fields = ["name"]

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