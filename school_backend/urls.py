
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Existing Django administration
    path("admin/", admin.site.urls),

    # Existing public school website API
    path("api/", include("school.urls")),

    # Existing admissions API
    path("api/admissions/", include("admissions.urls")),

    # New protected administration portal API
    path(
        "api/administration/",
        include("administration.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
