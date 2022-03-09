from django.contrib import admin
from django.urls import path, include
# from .import settings
# from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]

# urlpatterns += static(
#     settings.MEDIA_URL,
#     document_root=settings.MEDIA_ROOT
# )
# urlpatterns += static(
#     settings.STATIC_URL,
#     document_root=settings.STATIC_ROOT
# )
