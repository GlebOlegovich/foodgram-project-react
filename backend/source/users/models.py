
# from __future__ import annotations
from urllib import request

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Sum

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

    def _clean_up_shopping_cart(self):
        self.purchases.all().delete()

    def _get_user_shopping_cart(self):

        purchases = self.purchases
        if not purchases.exists():
            return None
        user_recipes_for_shopping = [
            purchase.recipe.name for purchase in purchases.all()
        ]

        # Возвращается список покупок
        # Каждый пункт покупки в виде словаря

        # Пришлось делать костыиль, если делал
        # from recipes.models import IngredientInRecipe
        # кидало ошибку
        # django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL
        # refers to model'users.User' that has not been installed
        shopping_cart = recipes.models.IngredientInRecipe.objects.filter(
            recipe__purchases__user=self
        ).values(
            ingredient_name=F('ingredient__name'),
            ingredient_measurement_unit=F('ingredient__measurement_unit'),
        ).annotate(
            ingredient_amount=Sum('amount'),
        ).order_by('ingredient_name')

        list = {
            'recipes_in_cart': user_recipes_for_shopping,
            'purchases': shopping_cart
        }
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
