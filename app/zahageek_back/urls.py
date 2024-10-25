from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/', include('authentication.urls')),
    path('api/freud/', include('freud.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
