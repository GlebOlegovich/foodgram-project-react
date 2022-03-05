from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins, generics
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    # GetTokenSerialiser,
    UsersListSerialiser,
    UserRegistrationSerializer,
    UserInfoSerialiser,
                          )
from .paginators import UsersCustomPagination
from .mixins import CreateUserMixin

User = get_user_model()

# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def registration_user(request):
#     serializer = UserRegistrationSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         user = serializer.save()
#         return Response(
#             {
#                 "email": user.email,
#                 "id": user.id,
#                 "username": user.username,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name
#             },
#             status=status.HTTP_201_CREATED
#         )
#     # valid_data = dict(serializer.validated_data)
#     # user = User()
#     else:
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


@action(detail=True, methods=["LIST", "POST"])
class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  CreateUserMixin,
                  viewsets.GenericViewSet):
    # lookup_field = "pk"
    lookup_url_kwarg = "id"
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UsersListSerialiser
    pagination_class = UsersCustomPagination

    def get_serializer_class(self):
        # if self.action in ("me",):
        #     return UserInfoSerialiser

        # Было бы круто сделать переадресацию, по типу:
        # Запрос от юзера с id = 3, на страницу users/3
        # Что бы редиректило на users/me
        if self.action in ("list", "retrieve", "me"):
            return UsersListSerialiser
        if self.action in ("create",):
            return UserRegistrationSerializer

    @action(
        detail=False,
        methods=["get"],
        serializer_class=UserInfoSerialiser,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# Post & Delete
class Subscribe(APIView):
    permission_classes = (IsAuthenticated,)

    def _get_author_and_user(self, request, author_id):
        return(
            get_object_or_404(User, id=author_id),
            request.user
        )

    # Проверка подписки юзера на автора
    def _check_user_is_author(self, user, author):
        return user == author

    def _check_user_is_trying_to_follow_himself(self, user, author):
        is_trying = self._check_user_is_author(user, author)
        message = (
            {
                "error":
                "Невозможно подписаться на самого себя!"
            } if is_trying else {}
        )
        return (is_trying, message)

    def _check_user_is_trying_to_unfollow_himself(self, user, author):
        is_trying = self._check_user_is_author(user, author)
        message = (
            {
                "error":
                "Невозможно отписаться от самого себя!"
            } if is_trying else {}
        )
        return (is_trying, message)

    def _check_user_is_not_following_author(self, user, author):
        is_not_following = not user._is_following(author)
        message = (
            {
                "error":
                "Невозможно отписаться, вы не были подписаны "
                f"на {author}!"
            } if is_not_following else {}
        )
        return(is_not_following, message)

    def _check_user_is_following_author(self, user, author):
        is_following = user._is_following(author)
        message = (
            {
                "error":
                "Невозможно подписаться, вы уже подписаны "
                f"на {author}!"
            } if is_following else {}
        )
        return(is_following, message)

    def _send_error_message(self, first, first_messare, second, second_message):
        if first or second:
            message = (
               first_messare if first
               else second_message
            )
            return (
                True,
                Response(
                    message,
                    status=status.HTTP_400_BAD_REQUEST
                )
            )
        return False, None

    # Подписаться
    def post(self, request, author_id):
        author, user = self._get_author_and_user(request, author_id)
        # print(inspect.currentframe().f_code.co_name)
        is_following, message_is_following = (
            self._check_user_is_following_author(user, author)
        )

        (
            is_trying_to_follow_himself,
            message_is_trying_to_follow_himself
        ) = (
            self._check_user_is_trying_to_follow_himself(user, author)
        )

        send, response = self._send_error_message(
            is_trying_to_follow_himself,
            message_is_trying_to_follow_himself,
            is_following, message_is_following
        )
        if send:
            return response
        user._follow(author)
        serializer = UsersListSerialiser(author)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    # Отписаться
    def delete(self, request, author_id):
        author, user = self._get_author_and_user(request, author_id)
        is_not_following, message_is_not_following = (
            self._check_user_is_not_following_author(user, author)
        )

        (
            is_trying_to_unfollow_himself,
            message_is_trying_to_unfollow_himself
        ) = (
            self._check_user_is_trying_to_unfollow_himself(user, author)
        )

        send, response = self._send_error_message(
            is_trying_to_unfollow_himself,
            message_is_trying_to_unfollow_himself,
            is_not_following, message_is_not_following
        )
        if send:
            return response
        user._unfollow(author)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSubscriptions(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    # queryset = request.user.objects.following.all()
    # Надо добавить еще рецепты юзеров что бы выводились
    serializer_class = UsersListSerialiser
    pagination_class = UsersCustomPagination

    def get_queryset(self):
        user = self.request.user
        user_is_follower = user.follower.all()
        followings = User.objects.filter(
            id__in=user_is_follower.values('author')).all()
        return followings
