
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from .serializers_user import UserInfoSerialiser


class CreateUserMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = UserInfoSerialiser(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            instance_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    # Пришлось сделать так, что бы как то получать экзмепляр модели,
    # только что созданный
    def perform_create(self, serializer):
        return serializer.save()
