from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from Foodgram.settings import GLOBAL_SETTINGS

from .validators import NotMeUsername, UsernameValidator


class User(AbstractUser):

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
            UnicodeUsernameValidator(),
            NotMeUsername(),
            UsernameValidator()
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

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"

    @property
    def _is_admin(self):
        return self.role == GLOBAL_SETTINGS["admin"] or self.is_superuser

    # @property
    # def _is_moderator(self):
    #     return self.role == GLOBAL_SETTINGS["moderator"] or self._is_admin
