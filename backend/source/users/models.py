
# from __future__ import annotations
from django.contrib.auth.models import AbstractUser
from django.db import models

import recipes as recipes
from config.settings import GLOBAL_SETTINGS

from .managers import CustomUserManager
# from recipes.models import IngredientInRecipe
from .validators import (NotDeletedUsernameValidator, NotMeUsernameValidator,
                         UsernameValidator)


# Пример по созданию кастомной модели юзера
# https://webdevblog.ru/
# sovremennyj-sposob-sozdanie-polzovatelskoj-modeli-user-v-django/
class User(AbstractUser):

    # username = LowercaseUsernameField(
    username = models.CharField(
        "Username",
        max_length=150,
        unique=True,
        help_text=(
            "Введите username, под которым будете, в дальнейшем, заходить "
            "на наш проект. Username может состоять из символов латинского "
            "алфавита [a-z A-Z], цифр [0-9] и спецсимволов: [ @ + - ]"
        ),
        validators=[
            # UnicodeUsernameValidator(),
            NotMeUsernameValidator(),
            UsernameValidator(),
            NotDeletedUsernameValidator()
        ],
        error_messages={
            "unique": (
                "Пользователь с таким username уже есть, включите фантазию и "
                "придумайте другой username."
            ),
        },
    )
    email = models.EmailField(
        "Электронная почта",
        unique=True,
        max_length=254,
        error_messages={
            "unique": "Пользователь с таким email уже создан",
        }
    )

    first_name = models.CharField(
        "Имя",
        max_length=50,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=50,
    )
    role = models.CharField(
        "Роль - права доступа",
        max_length=10,
        choices=GLOBAL_SETTINGS["ROLE"],
        default=GLOBAL_SETTINGS["user"]
    )
    objects = CustomUserManager()

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    @property
    def _is_admin(self):
        return self.role == GLOBAL_SETTINGS["admin"] or self.is_superuser

    def _is_following(self, obj):
        return Follow.objects.filter(
            user=self,
            author=obj
        ).exists()

    def _follow(self, obj):
        Follow.objects.get_or_create(
            user=self,
            author=obj
        )

    def _unfollow(self, obj):
        Follow.objects.filter(
            user=self,
            author=obj
        ).delete()

    @property
    def _get_user_shopping_cart(self):
        shopping_cart = self.purchases.all()
        if not shopping_cart.exists():
            return None
        list = {'recipes_in_cart': []}
        purchases = {}
        for item in shopping_cart:
            recipe = item.recipe
            # recipe_name = recipe.name
            if recipe.name not in list['recipes_in_cart']:
                list['recipes_in_cart'].append(recipe)
            # Пришлось делать костыиль, если делал
            # from recipes.models import IngredientInRecipe
            # кидало ошибку
            # django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL
            # refers to model'users.User' that has not been installed
            ingredients = recipes.models.IngredientInRecipe.objects.filter(
                recipe=recipe
            )
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in purchases:
                    purchases[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    purchases[name]['amount'] += amount
                    # (
                    #     list[name]['amount'] + amount
                    # )
        list['purchases'] = purchases
        return list

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """
    Модель подписок\n
    Пользователь, который подписывается - user\n
    На кого подписывается - author
    """
    # Пользователь, который подписывается
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь - кто подписан",
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь - на кого подписан",
        related_name="following"
    )

    class Meta:
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "user"],
                name="Follow_unique"
            ),
        ]

    def __str__(self):
        return f"{self.user} follows {self.author}"
