from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import HexColorValidator, TagSlugValidator

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингридиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Ингридиент'
        verbose_name = 'ингридиенты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        validators=[HexColorValidator(), ],
        unique=True
    )
    slug = models.CharField(
        'Уникальный слаг',
        max_length=200,
        validators=[TagSlugValidator(), ],
        unique=True
    )

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'
        constraints = [
            models.UniqueConstraint(fields=['name', 'slug'], name="Tag_unique")
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.slug}"


def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET(get_sentinel_user),
        verbose_name="Автор рецепта",
        related_name="recipes"
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        error_messages={
            'unique': ("Рецепт с таким названием уже создан."),
        },
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не может быть меньше 1 мин.'
            ), MaxValueValidator(32767)]
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name='Теги',
        # on_delete=models.SET_NULL,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe'
    )
    # Сортировать логичнее по дате публикации...
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name

    # Неожиданно для себя, понял что так работает)
    # Удаляет старые изображения из файловой системы
    def delete_image(self):
        self.image.delete()


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='get_ingredients')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='get_recipes')
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(1), MaxValueValidator(32767)]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='recipe_ingredient_unique',
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.ingredient} в рецепте {self.recipe} - {self.amount} "
            f"{self.ingredient.measurement_unit}"
        )
