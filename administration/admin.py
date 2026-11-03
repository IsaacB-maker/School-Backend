
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


class OwnerOnlyUserAdmin(UserAdmin):
    """
    Only the school owner can manage administrator accounts.
    Ordinary administrators cannot access Django Admin.
    """

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_superuser

    def save_model(self, request, obj, form, change):
        """
        Preserve the existing owner account.

        Every other administrator account is automatically
        kept as a non-staff, non-superuser account.
        """
        if obj.pk != request.user.pk:
            obj.is_staff = False
            obj.is_superuser = False

        super().save_model(request, obj, form, change)


class OwnerOnlyGroupAdmin(GroupAdmin):
    """
    Only the school owner can create and manage permission groups.
    """

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_active and request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_superuser


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, OwnerOnlyUserAdmin)
admin.site.register(Group, OwnerOnlyGroupAdmin)
