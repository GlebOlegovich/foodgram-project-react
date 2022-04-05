from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Recipe


class AddOrDeleteRecipeFromFavOrShoppingModelMixin:
    """
        Мда, название мб и плохое... Но это миксин для
        добавления/удаления
        рецепта в избранное/шопинг кард, например
    """
    def adding_recipe_to_model_with_serializer(
        self, request, recipe_id, root_serializer, *args, **kwargs
    ):
        '''
            Мда, название мб и плохое... Но это метод для добавления
            рецепта в избранное/шопинг кард, например
        '''
        user = request.user
        recipe = recipe = get_object_or_404(Recipe, id=recipe_id)

        data = {

            'user': user.id,

            'recipe': recipe.id,

        }
        serializer = root_serializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe_from_model(
        self, request, recipe_id, model, *args, **kwargs
    ):
        '''
            Мда, название мб и плохое... Но это метод для удаления
            рецепта в избранное/шопинг кард, например
        '''
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        instance = get_object_or_404(
            model, user=user, recipe=recipe
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
