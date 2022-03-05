from django.urls import include, path

# from .views import UpdatePassword

app_name = 'authentication'

urlpatterns = [
    path('', include('djoser.urls.authtoken')),
    # path('set_password/', UpdatePassword.as_view(), name=('set_password')),
]
