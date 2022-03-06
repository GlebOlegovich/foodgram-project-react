from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import UsersListSerialiser
from .models import Ingredient, Tag, Recipe, IngredientInRecipe

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    author = UsersListSerialiser(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(many=True, source='get_ingredients')
    # tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ('__all__')

    # image = Base64ImageField()
    # author = UserSerializer(read_only=True)
    # tags = TagSerializer(many=True, read_only=True)
    # ingredients = IngredientInRecipeSerializer(
    #     source='ingredients_amounts',
    #     many=True, read_only=True,
    # )
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    # class Meta:
    #     model = Recipe
    #     fields = ('id', 'tags', 'author', 'name', 'text',
    #               'image', 'ingredients', 'cooking_time',
    #               'is_favorited', 'is_in_shopping_cart')

    # def get_is_favorited(self, obj):
    #     request = self.context.get('request')
    #     if request is None or request.user.is_anonymous:
    #         return False
    #     return Favorites.objects.filter(user=request.user,
    #                                     recipe=obj).exists()

    # def get_is_in_shopping_cart(self, obj):
    #     request = self.context.get('request')
    #     if request is None or request.user.is_anonymous:
    #         return False
    #     return Purchase.objects.filter(user=request.user,
    #                                    recipe=obj).exists()