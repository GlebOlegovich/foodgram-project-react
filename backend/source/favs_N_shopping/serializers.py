from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe

from .models import Favorites, Purchase

User = get_user_model()


class FavoritORInShopingCart_RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoritesSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorites
        fields = ('user', 'recipe')

    def validate(self, data):
        print(data)
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        favorite_exists = Favorites.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'GET' and favorite_exists:
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FavoritORInShopingCart_RecipeSerializer(
            instance.recipe,
            context=context).data


class PurchaseSerializer(FavoritesSerializer):
    class Meta(FavoritesSerializer.Meta):
        model = Purchase

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        purchase_exists = Purchase.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'GET' and purchase_exists:
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FavoritORInShopingCart_RecipeSerializer(
            instance.recipe,
            context=context).data
