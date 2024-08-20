# steesh URL Configuration

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("main.urls")),
    path("owner/", include("owners.urls")),
    path("user/", include("users.urls")),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)