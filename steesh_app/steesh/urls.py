# steesh URL Configuration

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path("", include("main.urls")),
    # path("owner/", include("owners.urls")),
    # path("user/", include("users.urls")),
    path('api/', include('steesh_api.urls')),
    
 ]