
import json

from django import forms
from django.db import transaction, models
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from school.models import (
    AboutSchool,
    AcademicAssessment,
    AcademicLevel,
    AcademicPage,
    AcademicSubject,
    AcademicSupport,
    ContactSettings,
    CoreValue,
    Event,
    Gallery,
    News,
    SchoolSettings,
    Staff,
    TeachingApproach,
    WhyChooseUs,
)

from admissions.models import Application, Payment


# =========================================================
# APPROVED ADMINISTRATION RESOURCES
# =========================================================

ADMIN_RESOURCES = {
    "school-settings": SchoolSettings,
    "news": News,
    "events": Event,
    "gallery": Gallery,
    "staff": Staff,
    "contact-settings": ContactSettings,
    "about-school": AboutSchool,
    "core-values": CoreValue,
    "why-choose-us": WhyChooseUs,
    "academic-page": AcademicPage,
    "academic-levels": AcademicLevel,
    "academic-subjects": AcademicSubject,
    "academic-assessments": AcademicAssessment,
    "academic-support": AcademicSupport,
    "teaching-approaches": TeachingApproach,
    "applications": Application,
    "payments": Payment,
}


# =========================================================
# AUTHENTICATION AND PERMISSIONS
# =========================================================

def can_access_admin_portal(user):
    if not user.is_authenticated or not user.is_active:
        return False

    if user.is_superuser:
        return True

    return (
        user.has_module_perms("school")
        or user.has_module_perms("admissions")
    )


def administrator_data(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_owner": user.is_superuser,
        "is_staff": user.is_staff,
        "permissions": sorted(user.get_all_permissions()),
    }


def has_resource_permission(user, model, action):
    if not can_access_admin_portal(user):
        return False

    if user.is_superuser:
        return True

    permission = (
        f"{model._meta.app_label}."
        f"{action}_{model._meta.model_name}"
    )

    return user.has_perm(permission)


def authentication_required():
    return JsonResponse(
        {"detail": "Administrator authentication required."},
        status=401,
    )


def permission_denied():
    return JsonResponse(
        {"detail": "You do not have permission to perform this action."},
        status=403,
    )


# =========================================================
# AUTHENTICATION ENDPOINTS
# =========================================================

@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({
        "csrfToken": get_token(request),
    })


@require_POST
@csrf_protect
def admin_login(request):
    try:
        data = json.loads(request.body or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"detail": "Invalid request data."},
            status=400,
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {"detail": "Invalid request data."},
            status=400,
        )

    username = str(data.get("username", "")).strip()
    password = data.get("password", "")

    if not username or not isinstance(password, str) or not password:
        return JsonResponse(
            {"detail": "Username and password are required."},
            status=400,
        )

    user = authenticate(
        request,
        username=username,
        password=password,
    )

    if user is None or not can_access_admin_portal(user):
        return JsonResponse(
            {
                "detail": (
                    "Invalid login credentials or "
                    "insufficient access."
                )
            },
            status=401,
        )

    login(request, user)

    return JsonResponse({
        "detail": "Login successful.",
        "user": administrator_data(user),
    })


@require_POST
@csrf_protect
def admin_logout(request):
    if not request.user.is_authenticated:
        return authentication_required()

    logout(request)

    return JsonResponse({
        "detail": "Logout successful.",
    })


@require_GET
def admin_me(request):
    if not can_access_admin_portal(request.user):
        return authentication_required()

    return JsonResponse({
        "user": administrator_data(request.user),
    })


# =========================================================
# RESOURCE SERIALIZATION
# =========================================================

def serialize_record(instance):
    result = {
        "id": instance.pk,
    }

    for field in instance._meta.concrete_fields:
        if field.primary_key:
            continue

        value = getattr(instance, field.attname)

        if isinstance(field, models.FileField):
            file_value = getattr(instance, field.name)

            try:
                value = file_value.url if file_value else None
            except ValueError:
                value = None

        elif hasattr(value, "isoformat"):
            value = value.isoformat()

        result[field.name] = value

    return result


# =========================================================
# REQUEST DATA
# =========================================================

def get_request_data(request):
    content_type = request.content_type or ""

    if content_type == "application/json":
        try:
            data = json.loads(request.body or "{}")
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None, None

        if not isinstance(data, dict):
            return None, None

        return data, request.FILES

    if content_type.startswith("multipart/form-data"):
        return request.POST, request.FILES

    if content_type == "application/x-www-form-urlencoded":
        return request.POST, request.FILES

    return None, None


# =========================================================
# RESOURCE LIST AND CREATE
# =========================================================

@csrf_protect
def resource_list(request, resource):
    model = ADMIN_RESOURCES.get(resource)

    if model is None:
        return JsonResponse(
            {"detail": "Resource not found."},
            status=404,
        )

    if request.method == "GET":

        if not has_resource_permission(
            request.user, model, "view"
        ):
            if not request.user.is_authenticated:
                return authentication_required()

            return permission_denied()

        queryset = model.objects.all()

        search = request.GET.get("search", "").strip()

        if search:
            search_query = Q()

            for field in model._meta.fields:
                if isinstance(
                    field,
                    (models.CharField, models.TextField),
                ):
                    search_query |= Q(**{
                        f"{field.name}__icontains": search
                    })

            queryset = queryset.filter(search_query)

        try:
            limit = min(
                max(int(request.GET.get("limit", 100)), 1),
                200,
            )

            offset = max(
                int(request.GET.get("offset", 0)),
                0,
            )

        except (ValueError, TypeError):
            return JsonResponse(
                {"detail": "Invalid pagination values."},
                status=400,
            )

        total = queryset.count()

        records = [
            serialize_record(item)
            for item in queryset[offset:offset + limit]
        ]

        return JsonResponse({
            "resource": resource,
            "total": total,
            "results": records,
        })

    if request.method == "POST":

        if not has_resource_permission(
            request.user, model, "add"
        ):
            if not request.user.is_authenticated:
                return authentication_required()

            return permission_denied()

        data, files = get_request_data(request)

        if data is None:
            return JsonResponse(
                {"detail": "Use JSON or multipart form data."},
                status=400,
            )

        form_class = forms.modelform_factory(
            model,
            fields="__all__",
        )

        form = form_class(data, files)

        if not form.is_valid():
            return JsonResponse(
                {
                    "detail": "Validation failed.",
                    "errors": form.errors,
                },
                status=400,
            )

        with transaction.atomic():
            instance = form.save()

        return JsonResponse(
            {
                "detail": "Record created successfully.",
                "record": serialize_record(instance),
            },
            status=201,
        )

    return JsonResponse(
        {"detail": "Method not allowed."},
        status=405,
    )


# =========================================================
# RESOURCE FORM FIELD METADATA
# =========================================================

@require_GET
def resource_schema(request, resource):
    if not request.user.is_authenticated:
        return authentication_required()

    model = ADMIN_RESOURCES.get(resource)

    if model is None:
        return JsonResponse(
            {"detail": "Resource not found."},
            status=404,
        )

    action = request.GET.get("action", "add")

    if action not in ("add", "change"):
        return JsonResponse(
            {"detail": "Invalid form action."},
            status=400,
        )

    if not has_resource_permission(
        request.user, model, action
    ):
        return permission_denied()

    fields = []

    for field in model._meta.concrete_fields:

        if field.primary_key or not field.editable:
            continue

        form_field = field.formfield()

        if form_field is None:
            continue

        if isinstance(field, models.ImageField):
            field_type = "image"

        elif isinstance(field, models.FileField):
            field_type = "file"

        elif isinstance(field, models.ForeignKey):
            field_type = "select"

        elif isinstance(field, models.BooleanField):
            field_type = "boolean"

        elif isinstance(field, models.DateTimeField):
            field_type = "datetime"

        elif isinstance(field, models.DateField):
            field_type = "date"

        elif isinstance(field, models.TimeField):
            field_type = "time"

        elif isinstance(field, models.DecimalField):
            field_type = "number"

        elif isinstance(field, models.FloatField):
            field_type = "number"

        elif isinstance(field, models.IntegerField):
            field_type = "number"

        elif isinstance(field, models.TextField):
            field_type = "textarea"

        elif isinstance(field, models.EmailField):
            field_type = "email"

        elif isinstance(field, models.URLField):
            field_type = "url"

        else:
            field_type = "text"

        field_data = {
            "name": field.name,
            "label": str(field.verbose_name).title(),
            "type": field_type,
            "required": form_field.required,
            "help_text": str(field.help_text),
        }

        if isinstance(field, models.ForeignKey):

            related_model = field.remote_field.model

            if not has_resource_permission(
                request.user, related_model, "view"
            ):
                return permission_denied()

            related_records = related_model.objects.all()[:500]

            field_data["options"] = [
                {
                    "value": record.pk,
                    "label": str(record),
                }
                for record in related_records
            ]

        elif field.choices:

            field_data["options"] = [
                {
                    "value": value,
                    "label": str(label),
                }
                for value, label in field.flatchoices
                if value not in ("", None)
            ]

        if getattr(field, "max_length", None):
            field_data["max_length"] = field.max_length

        if isinstance(field, models.DecimalField):
            field_data["decimal_places"] = field.decimal_places

        fields.append(field_data)

    return JsonResponse({
        "resource": resource,
        "model": model._meta.verbose_name.title(),
        "action": action,
        "fields": fields,
    })


# =========================================================
# RESOURCE DETAIL, UPDATE AND DELETE
# =========================================================

@csrf_protect
def resource_detail(request, resource, pk):

    model = ADMIN_RESOURCES.get(resource)

    if model is None:
        return JsonResponse(
            {"detail": "Resource not found."},
            status=404,
        )

    if not request.user.is_authenticated:
        return authentication_required()

    try:
        instance = model.objects.get(pk=pk)

    except model.DoesNotExist:
        return JsonResponse(
            {"detail": "Record not found."},
            status=404,
        )

    # -----------------------------------------------------
    # RETRIEVE ONE RECORD
    # -----------------------------------------------------

    if request.method == "GET":

        if not has_resource_permission(
            request.user, model, "view"
        ):
            return permission_denied()

        return JsonResponse({
            "resource": resource,
            "record": serialize_record(instance),
        })

    # -----------------------------------------------------
    # UPDATE ONE RECORD
    # -----------------------------------------------------

    if request.method in ("PUT", "PATCH"):

        if not has_resource_permission(
            request.user, model, "change"
        ):
            return permission_denied()

        data, files = get_request_data(request)

        if data is None:
            return JsonResponse(
                {"detail": "Use JSON or multipart form data."},
                status=400,
            )

        if request.method == "PATCH":

            merged_data = {}

            for field in model._meta.concrete_fields:

                if field.primary_key or not field.editable:
                    continue

                if isinstance(field, models.FileField):
                    continue

                merged_data[field.name] = getattr(
                    instance,
                    field.attname,
                )

            merged_data.update(dict(data.items()))
            data = merged_data

        form_class = forms.modelform_factory(
            model,
            fields="__all__",
        )

        form = form_class(
            data=data,
            files=files,
            instance=instance,
        )

        if not form.is_valid():
            return JsonResponse(
                {
                    "detail": "Validation failed.",
                    "errors": form.errors,
                },
                status=400,
            )

        with transaction.atomic():
            updated_instance = form.save()

        return JsonResponse({
            "detail": "Record updated successfully.",
            "record": serialize_record(updated_instance),
        })

    # -----------------------------------------------------
    # DELETE ONE RECORD
    # -----------------------------------------------------

    if request.method == "DELETE":

        if not has_resource_permission(
            request.user, model, "delete"
        ):
            return permission_denied()

        application_id = None

        is_payment = (
            model._meta.label_lower == "admissions.payment"
        )

        if is_payment:
            application_id = instance.application_id

        with transaction.atomic():

            instance.delete()

            # Recalculate the application payment status
            # after deleting a payment record.

            if is_payment and application_id is not None:

                application_model = (
                    model._meta
                    .get_field("application")
                    .remote_field.model
                )

                application = (
                    application_model.objects
                    .select_for_update()
                    .get(pk=application_id)
                )

                remaining_statuses = set(
                    model.objects.filter(
                        application_id=application_id
                    ).values_list("status", flat=True)
                )

                if "paid" in remaining_statuses:
                    new_status = "paid"

                elif "processing" in remaining_statuses:
                    new_status = "processing"

                elif "pending" in remaining_statuses:
                    new_status = "pending"

                elif "refunded" in remaining_statuses:
                    new_status = "refunded"

                elif "failed" in remaining_statuses:
                    new_status = "failed"

                else:
                    new_status = "pending"

                application.payment_status = new_status

                application.save(
                    update_fields=[
                        "payment_status",
                        "updated_at",
                    ]
                )

        return JsonResponse({
            "detail": "Record deleted successfully.",
        })

    return JsonResponse(
        {"detail": "Method not allowed."},
        status=405,
    )
