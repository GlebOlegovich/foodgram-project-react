import unicodedata
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(
        self, username, email, password,
        **extra_fields
    ):
        # Если честно, не очень понимаю зачем тут эти проверки...
        # Но они юзаются вот тут, например
        # from django.contrib.auth.models import UserManager
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email).lower()
        if not username:
            raise ValueError("The given username must be set")
        username = self.normalize_username(username).lower()
        if not password:
            raise ValueError('Введите пароль!')
        user = self.model(
            email=email,
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self, username, email=None,
        password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        ).lower()
