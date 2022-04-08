from rest_framework import serializers

from django.contrib.auth import get_user_model

from recipes.models import Recipe
from recipes.serializers import FavoritORInShopingCartRecipeSerializer

from .models import Follow

User = get_user_model()

# Пришлось сделать это отдельным файлом, потому что я тут
# импортирую FavoritORInShopingCartRecipeSerializer,
# а в recipes.serializers импортируется UsersListSerialiser
# из serializers_user (бывшего serializers) и был циклический импорт...
# ImportError: cannot import name 'FavoritORInShopingCartRecipeSerializer'
#  from partially initialized module 'recipes.serializers'
# (most likely due to a circular import)


class FollowerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    # id = serializers.ReadOnlyField(source='author.id')
    # email = serializers.ReadOnlyField(source='author.email')
    # username = serializers.ReadOnlyField(source='author.username')
    # first_name = serializers.ReadOnlyField(source='author.first_name')
    # last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj).all()
        if not queryset.exists():
            return None

        if limit is not None:
            queryset = Recipe.objects.filter(
                author=obj
            )[:int(limit)]

        return FavoritORInShopingCartRecipeSerializer(
            queryset, many=True
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
