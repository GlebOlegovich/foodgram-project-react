from django.urls import include, path
# from django.conf.urls import url

app_name = 'auth'

urlpatterns = [
    path('users/', include('users.urls')),
    path('auth/', include('auth.urls')),
]
