from django.urls import include, path

app_name = 'auth'

# НЕ СДЕЛАНО ИЗМЕНЕНИЕ ПАРОЛЯ!
urlpatterns = [
    path('', include('djoser.urls.authtoken')),
]
