from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ChangePasswordSerializer


class UpdatePassword(APIView):
    '''
        Смена пасса. Post запрос.
    '''
    permission_classes = (IsAuthenticated, )

    def _get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self._get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            # Проверка старого пароля
            current_password = serializer.data.get("current_password")
            if not self.object.check_password(current_password):
                return Response({"current_password": ["Неверный пароль!"]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password хэширует пасс юзера!
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
