# Generated by Django 4.0.3 on 2022-04-04 13:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Количество ингредиентов не может быть меньше 1.'), django.core.validators.MaxValueValidator(32767, message='Количество ингредиентов не может быть больше 32767.')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Время приготовления не может быть меньше 1 мин.'), django.core.validators.MaxValueValidator(32767, message='Время приготовления не может быть больше 32767 мин.')], verbose_name='Время приготовления (в минутах)'),
        ),
    ]