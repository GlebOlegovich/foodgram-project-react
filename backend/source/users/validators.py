from django.core import validators
from django.utils.deconstruct import deconstructible


# Надо сделать ограничение на юзернейм, только Английский алфавит!

@deconstructible
class UsernameValidator(validators.RegexValidator):
    # В тз так, но тогда можно сделать username "Петрович"...
    # Короче говоря, поддерживает еще и кириллицу
    # regex = r"^[\w.@+-]+$"
    regex = r"^[a-zA-Z0-9@+-]+$"
    message = (
        "Вы ввели невалидный username!\n"
        "Username может состоять из символов латинского "
        "алфавита [a-z A-Z], цифр [0-9] и спецсимволов: [ @ + - ]"
    )
    flags = 0


@deconstructible
class NotMeUsernameValidator(validators.RegexValidator):
    """
    Userneme != "Me"
    """
    regex = r"^(?!Me$|me$|ME$|mE$).*$"
    message = ("Userneme не может быть - Me")
    flags = 0


@deconstructible
class NotDeletedUsernameValidator(validators.RegexValidator):
    """
    Userneme != "Deleted"
    """
    regex = r"^(?!(?i:deleted)).*$"
    message = ("Userneme не может быть - Deleted")
    flags = 0
