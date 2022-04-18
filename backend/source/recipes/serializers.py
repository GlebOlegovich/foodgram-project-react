# Для сохранени изображения из base64
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db.models import F

from users.serializers_user import UsersListSerialiser

from .models import (Favorite, Ingredient, IngredientInRecipe, Purchase,
                     Recipe, Tag)

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


class FavoritORInShopingCartRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        favorite_exists = Favorite.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'POST' and favorite_exists:
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FavoritORInShopingCartRecipeSerializer(
            instance.recipe,
            context=context).data


class PurchaseSerializer(FavoriteSerializer):
    class Meta(FavoriteSerializer.Meta):
        model = Purchase

    def validate(self, data):
        request = self.context.get('request')
        recipe_id = data['recipe'].id
        purchase_exists = Purchase.objects.filter(
            user=request.user,
            recipe__id=recipe_id
        ).exists()

        if request.method == 'POST' and purchase_exists:
            raise serializers.ValidationError(
                'Рецепт уже в списке покупок'
            )

        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FavoritORInShopingCartRecipeSerializer(
            instance.recipe,
            context=context).data


class RecipeListSerializer(serializers.ModelSerializer):
    author = UsersListSerialiser(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngredientInRecipe.objects.filter(recipe=obj)
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Purchase.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'name', 'text',
                  'image',
                  'ingredients', 'cooking_time')
        read_only_fields = ('author',)

    def to_representation(self, instance):
        serializer = RecipeListSerializer(instance)
        return serializer.data

    # Вроде бы должно подтянуться из модели рецепта, но почему то нет...
    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Время приготовления должно быть целым числом больше 0!'
            )
        if value > 32767:
            raise serializers.ValidationError(
                'Время приготовления должно быть целым числом меньше 32768!'
            )
        return value

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError('Укажите ингредиенты!')
        ingredients_set = list()
        for ingredient in ingredients:
            ingredient_obj = ingredient.get('id')
            amount = ingredient.get('amount')
            if amount <= 0:
                raise serializers.ValidationError(
                    'Убедитесь, что значение количества '
                    f'ингредиента "{ingredient_obj.name}" больше 0'
                )
            if amount > 32767:
                raise serializers.ValidationError(
                    'Убедитесь, что значение количества '
                    f'ингредиента "{ingredient_obj.name}" меньше 32768'
                )
            if ingredient_obj.id in ingredients_set:
                raise serializers.ValidationError(
                    f'Ингредиент "{ingredient_obj.name}" '
                    'в рецепте не должен повторяться.'
                )

            ingredients_set.append(ingredient_obj.id)
        return ingredients

    def validate_tags(self, tags):
        # Т.к. теперь у нас PrimaryKeyRelatedField, проверка,
        # что такой тэг есть не нужна
        if len(tags) > len(set(tags)):
            raise serializers.ValidationError(
                'Повторяющихся тегов в одном рецепе быть не должно!'
            )
        return tags

    def _add_ingredients_in_recipe(self, recipe, ingredients):
        # https://docs.djangoproject.com/en/4.0/ref/models/
        # querysets/#bulk-create
        temp_ingredients = list()
        # bulk-create не делает нумерацию pk
        obj_id = (
            IngredientInRecipe.objects.latest('id').id + 1
            if IngredientInRecipe.objects.all().exists()
            else 0
        )
        for ingredient in ingredients:
            # Это я дебажил час... из за PrimaryKeyRelatedField у
            # тегов - возвращался объект, хоть мы его и брали по 'id',
            # а нам нужен был id
            ingredient_id = ingredient.get('id').id
            amount = ingredient.get('amount')

            temp_ingredients.append(
                IngredientInRecipe(
                    id=obj_id,
                    recipe=recipe,
                    ingredient_id=ingredient_id,
                    amount=amount
                )
            )
            obj_id += 1

        IngredientInRecipe.objects.bulk_create(
            temp_ingredients,
            # Это максимум для SqLite
            batch_size=999
        )

    # На случай, если захотим снять ограничение,
    # на повторение ингредиентов и сделать их сложение,
    # но тут уже без bulk_create
    def _add_ingredients_in_recipe_no_restrictions_on_uniqueness(
        self, recipe, ingredients
    ):
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id').id
            amount = ingredient.get('amount')
            if IngredientInRecipe.objects.filter(
                recipe=recipe,
                ingredient=ingredient_id
            ).exists():
                amount += F('amount')
            # https://stackoverflow.com/questions/16329946/
            # django-model-method-create-or-update
            IngredientInRecipe.objects.update_or_create(
                recipe=recipe, ingredient=ingredient_id,
                defaults={'amount': amount}
            )

    def create(self, validated_data):
        # Попаю, что бы в самом конце созранить фотку, мало ли какие
        # то ошибки будет, а фотка улетит уже в media, нам не нужны
        # лишниее фотки...
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        # Если проблемы с получением из validated_data:
        # 8 пункт
        # https://profil-software.com/blog/development/
        # 10-things-you-need-know-effectively-use-django-rest-framework/#l3iqd
        # self.initial_data.get('ingredients')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self._add_ingredients_in_recipe(recipe, ingredients)
        recipe.image = image
        # Иначе фотка не сохранялась
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        IngredientInRecipe.objects.filter(recipe=instance).delete()
        self._add_ingredients_in_recipe(instance, ingredients)

        # tags - many2many field, .set() устанавливает новые значения всегда
        instance.tags.set(tags)

        return super().update(instance, validated_data)
