from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class UsersListSerialiser(serializers.ModelSerializer):
    ''' Инфа о других юзерах, с полем is_subscribed, для LIST и DETAIL'''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email", "id", "username", "first_name", "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if (
            request
            and hasattr(request, "user")
            and request.user.is_authenticated
        ):
            # Вообще наверное это плохая реализация,
            # каждый раз запрашиваем из БД
            return request.user.follower.filter(author=obj).exists()
        else:
            # Я хз что еще возвращать, если не авторизован
            return False


class UserInfoSerialiser(serializers.ModelSerializer):
    ''' Инфа о юзере, после регистрации'''
    class Meta:
        model = User
        fields = (
            "email", "id", "username", "first_name", "last_name"
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password", "first_name", "last_name"]

    def validate_username(self, value):
        lower_username = value.lower()
        if not(User.objects.filter(
            username__iexact=lower_username
        ).exists()):
            return value
        else:
            raise serializers.ValidationError(
                "Пользователь с таким Usernmae уже есть!"
            )

    def validate_email(self, value):
        lower_email = value.lower()
        if not (User.objects.filter(email__iexact=lower_email).exists()):
            return value
        else:
            raise serializers.ValidationError(
                "Пользователь с таким email уже есть!"
            )

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Проверяем на валидность пароль
        password = self.validated_data["password"]
        return User.objects.create_user(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            password=password
        )
        # Альтернатива, если без create_user
        # Через создание объекта модели
        # user = User(
        #     email=self.validated_data["email"],
        #     username=self.validated_data["username"],
        #     first_name=self.validated_data["first_name"],
        #     last_name=self.validated_data["last_name"],
        # )
        # # Сохраняем пароль
        # user.set_password(password)
        # user.save()
