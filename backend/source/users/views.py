from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins


from .serializers import (
    # GetTokenSerialiser,
    UsersListSerialiser,
    UserRegistrationSerializer,
                          )
from .paginators import UsersCustomPagination
from .mixins import CreateUserMixin

User = get_user_model()


# class ListUsers(generics.ListAPIView):
#     permission_classes = (AllowAny,)
#     queryset = User.objects.all()
#     serializer_class = UsersListSerialiser
#     pagination_class = UsersCustomPagination

# @api_view(['POST'])
# @permission_classes((AllowAny,))
# def registration_user(request):
#     serializer = UserRegistrationSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         user = serializer.save()
#         return Response(
#             {
#                 'email': user.email,
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


@action(detail=True, methods=['LIST', 'POST'])
class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  CreateUserMixin,
                  viewsets.GenericViewSet):
    # lookup_field = 'pk'
    lookup_url_kwarg = 'id'
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UsersListSerialiser
    pagination_class = UsersCustomPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return UsersListSerialiser
        if self.action in ('create',):
            return UserRegistrationSerializer

    @action(
        detail=False,
        methods=['get'],
        serializer_class=UsersListSerialiser,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
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
