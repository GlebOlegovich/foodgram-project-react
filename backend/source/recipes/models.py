from django.db import models


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


# class Recipe(models.Model):
#     pass


# class IngredientInRecipe(models.Model):
#     # amount = models.IntegerField()
#     pass

