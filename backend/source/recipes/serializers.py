from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# Для сохранени изображения из base64
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from favs_n_shopping.models import Favorite, Purchase
from users.serializers import UsersListSerialiser

from .models import Ingredient, IngredientInRecipe, Recipe, Tag

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
    image = Base64ImageField()
    author = UsersListSerialiser(read_only=True)
    # Добавление тега в рецепт делаем в create и update (POST/PUT запрос)
    tags = TagSerializer(many=True, read_only=True)
    # Аналогично тегу, поэтому read_only=True
    ingredients = IngredientInRecipeSerializer(
        many=True,
        read_only=True,
        source='get_ingredients'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text',
                  'image',
                  'ingredients', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user,
                                        recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Purchase.objects.filter(user=request.user,
                                       recipe=obj).exists()

    # В документации описано подробнее, расскажу вкратце
    # https://www.django-rest-framework.org/api-guide/serializers/#validation
    def validate(self, data):
        # 8 пункт
        # https://profil-software.com/blog/development/
        # 10-things-you-need-know-effectively-use-django-rest-framework/#l3iqd
        # ingredients = self.initial_data.get('ingredients')
        
        # Делал вот это
        # print(data)
        # Вывод был вот такой 
        # OrderedDict(
        #     [('name', '4'),
        #     ('text', 'йцв'),
        #     ('image', <SimpleUploadedFile:1.jpg (image/jpeg)>),
        #     ('cooking_time', 4)]
        # )
        # Я из data никак не могу взять ингридиенты...
        # Поэтому или:
        # request = self.context.get('request')
        # ingredients = request.data.get('ingredients')
        # или
        # 8 пункт
        # https://profil-software.com/blog/development/
        # 10-things-you-need-know-effectively-use-django-rest-framework/#l3iqd
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            try:
                get_object_or_404(Ingredient, id=ingredient['id'])
            except:
                raise serializers.ValidationError('Неизвестный ингридиент')
        # Проверка ингридиентов
        ingredients_set = set()
        for ingredient in ingredients:
            if int(ingredient.get('amount')) <= 0:
                raise serializers.ValidationError(
                    ('Убедитесь, что значение количества '
                     'ингредиента больше 0')
                )
            if int(ingredient.get('amount')) > 32767:
                raise serializers.ValidationError(
                    ('Убедитесь, что значение количества '
                     'ингредиента меньше 32768')
                )
            # django.db.utils.DataError: smallint out of range
            id = ingredient.get('id')
            if id in ingredients_set:
                raise serializers.ValidationError(
                    'Ингредиент в рецепте не должен повторяться.'
                )
            ingredients_set.add(id)
        data['ingredients'] = ingredients

        tags = self.initial_data.get('tags')
        for tag in tags:
            try:
                get_object_or_404(Tag, id=tag)
            except:
                raise serializers.ValidationError('Неизвестный Тег')
        data['tags'] = tags
        return data

    def create(self, validated_data):
        # Вообще, вроде бы можно не попать image, теперь
        image = validated_data.pop('image')

        # Необработанные входные данные в виде Dict - initial_data
        # tags = self.initial_data.get('tags')
        # или
        # Сделал в validate прокидывание тегов в валид дата
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        # recipe = Recipe.objects.create(image=image, **validated_data)
        recipe = Recipe.objects.create(**validated_data)
        try:
            self._add_ingredients_in_recipe(
                recipe=recipe,
                ingredients=ingredients
            )

            self._add_tags_in_recipe(
                recipe=recipe,
                tags=tags
                )

            recipe.image = image
        except:
            recipe.delete()
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        # tags = self.initial_data.get('tags')
        self._add_tags_in_recipe(
            recipe=instance,
            tags=validated_data.pop('tags')
            )

        IngredientInRecipe.objects.filter(recipe=instance).delete()
        self._add_ingredients_in_recipe(
            recipe=instance,
            ingredients=validated_data.pop('ingredients')
            )
        return super().update(instance, validated_data)
        # Заюзал супер, вместо прописывания руками.
        # if validated_data.get('image') is not None:
        #     instance.delete_image()
        #     instance.image = validated_data.get('image')
        # instance.name = validated_data.get('name')
        # instance.text = validated_data.get('text')
        # instance.cooking_time = validated_data.get('cooking_time')
        # instance.save()

        # return instance

    def _add_ingredients_in_recipe(self, recipe, ingredients):
        # заценить!
        # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#bulk-create
        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

    def _add_tags_in_recipe(self, recipe, tags):
        for tag in tags:
            if type(tag)==int:
                recipe.tags.add(get_object_or_404(Tag, pk=tag))
            else:
                raise serializers.ValidationError(
                    'Возникли проблемы с тегом, мы не получили id.'
                )