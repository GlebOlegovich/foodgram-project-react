from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+$"

    message = (
        "Вы ввели невалидный username!\n"
        "Username может состоять из символов латинского "
        "алфавита [a-z A-Z], цифр [0-9] и спецсимволов: [ @ + - ] "
    )
    flags = 0


@deconstructible
class NotMeUsername(validators.RegexValidator):
    """
    Userneme != "Me"
    """
    regex = r"^(?!Me$|me$|ME$|mE$).*$"
    message = ("Userneme не может быть - Me")
    flags = 0
