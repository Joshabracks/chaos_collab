from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from apps.main_app import views


urlpatterns = [
    url(r'^', include('apps.main_app.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)