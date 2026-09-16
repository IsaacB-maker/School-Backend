from django.contrib import admin

from .models import Application, Payment


class PaymentInline(admin.TabularInline):

    model = Payment

    extra = 1

    fields = (
        'amount',
        'payment_method',
        'reference',
        'status',
        'paid_at',
    )

    readonly_fields = (
        'paid_at',
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'application_number',
        'first_name',
        'last_name',
        'class_applying_for',
        'parent_phone',
        'status',
        'payment_status',
        'created_at',
    )

    list_filter = (
        'status',
        'payment_status',
        'gender',
        'class_applying_for',
        'created_at',
    )

    search_fields = (
        'application_number',
        'first_name',
        'last_name',
        'parent_name',
        'parent_phone',
        'parent_email',
    )

    readonly_fields = (
        'application_number',
        'created_at',
        'updated_at',
    )

    inlines = [
        PaymentInline,
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'application',
        'amount',
        'payment_method',
        'reference',
        'status',
        'created_at',
        'paid_at',
    )

    list_filter = (
        'status',
        'payment_method',
        'created_at',
    )

    search_fields = (
        'application__application_number',
        'application__first_name',
        'application__last_name',
        'reference',
    )

    readonly_fields = (
        'created_at',
    )