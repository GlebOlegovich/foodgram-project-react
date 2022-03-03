from django.urls import include, path

app_name = 'auth'

urlpatterns = [
    path('', include('djoser.urls.authtoken')),
]
