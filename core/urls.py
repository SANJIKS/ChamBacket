from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="ECO",
        default_version='v1',
        description="API for Ekoton",
        terms_of_service="https://youtube.com",
        contact=openapi.Contact(email="evionteam1@gmail.com"),
        license=openapi.License(name="Evion"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('user/', include('djoser.urls')),
    path('login/', include('djoser.urls.jwt')),
    path('', include('users.urls')),
    path('', include('partners.urls')),
    path('', include('backets.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)