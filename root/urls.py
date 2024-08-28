from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from root.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
