from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UsersListSerialiser(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', "first_name", "last_name", "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if (
            request
            and hasattr(request, "user")
            and request.user.is_authenticated
        ):
            user_follows = request.user.follower.all()
            return user_follows.filter(author=obj).exists()
        else:
            # Я хз что еще возвращать, если не авторизован
            return False


class UserInfoSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', "first_name", "last_name"
        )

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def validate_username(self, value):
        lower_username = value.lower()
        if not(User.objects.filter(
            username__iexact=lower_username
            ).exists()
        ):
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
        password = self.validated_data['password']
        user = User.objects.create_user(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            password=password
        )
        # Через создание объекта модели
        # user = User(
        #     email=self.validated_data['email'],
        #     username=self.validated_data['username'],
        #     first_name=self.validated_data['first_name'],
        #     last_name=self.validated_data['last_name'],
        # )
        # # Сохраняем пароль
        # user.set_password(password)
        # user.save()
        return user
