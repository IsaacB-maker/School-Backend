
from django.urls import path

from . import views

urlpatterns = [
    # Administrator authentication
    path("csrf/", views.csrf_token, name="admin-csrf"),
    path("login/", views.admin_login, name="admin-login"),
    path("logout/", views.admin_logout, name="admin-logout"),
    path("me/", views.admin_me, name="admin-me"),

    # Administration CRUD resources
    path(
        "resources/<slug:resource>/",
        views.resource_list,
        name="admin-resource-list",
    ),
    path(
        "resources/<slug:resource>/schema/",
        views.resource_schema,
        name="admin-resource-schema",
    ),
    path(
        "resources/<slug:resource>/<int:pk>/",
        views.resource_detail,
        name="admin-resource-detail",
    ),
]
