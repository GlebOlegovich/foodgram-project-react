from rest_framework import serializers

from django.contrib.auth import get_user_model

from favs_n_shopping.serializers import FavoritORInShopingCart_RecipeSerializer
from recipes.models import Recipe

from .models import Follow

User = get_user_model()


class UsersListSerialiser(serializers.ModelSerializer):
    ''' Инфа о других юзерах, с полем is_subscribed, для LIST и DETAIL'''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email", "id", "username", "first_name", "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if (
            request
            and hasattr(request, "user")
            and request.user.is_authenticated
        ):
            # Вообще наверное это плохая реализация,
            # каждый раз запрашиваем из БД
            user_follows = request.user.follower.filter(author=obj).exists()
            return user_follows
        else:
            # Я хз что еще возвращать, если не авторизован
            return False


class UserInfoSerialiser(serializers.ModelSerializer):
    ''' Инфа о юзере, после регистрации'''
    class Meta:
        model = User
        fields = (
            "email", "id", "username", "first_name", "last_name"
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password", "first_name", "last_name"]

    def validate_username(self, value):
        lower_username = value.lower()
        if not(User.objects.filter(
            username__iexact=lower_username
            ).exists()
        ):
            return value
        else:
            raise serializers.ValidationError(
                "Пользователь с таким Usernmae уже есть!"
            )

    def validate_email(self, value):
        lower_email = value.lower()
        if not (User.objects.filter(email__iexact=lower_email).exists()):
            return value
        else:
            raise serializers.ValidationError(
                "Пользователь с таким email уже есть!"
            )

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Проверяем на валидность пароль
        password = self.validated_data["password"]
        user = User.objects.create_user(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            password=password
        )
        # Через создание объекта модели
        # user = User(
        #     email=self.validated_data["email"],
        #     username=self.validated_data["username"],
        #     first_name=self.validated_data["first_name"],
        #     last_name=self.validated_data["last_name"],
        # )
        # # Сохраняем пароль
        # user.set_password(password)
        # user.save()
        return user


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

        return FavoritORInShopingCart_RecipeSerializer(
            queryset, many=True
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
