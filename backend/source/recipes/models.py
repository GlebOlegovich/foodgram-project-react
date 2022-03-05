from django.db import models

from .validators import TagSlugValidator, HexColorValidator


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
        validators=[HexColorValidator(),],
        unique=True
    )
    slug = models.CharField(
        'Уникальный слаг',
        max_length=200,
        validators=[TagSlugValidator(),],
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

# class Recipe(models.Model):
#     pass


# class IngredientInRecipe(models.Model):
#     # amount = models.IntegerField()
#     pass
