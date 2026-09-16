from django.urls import path

from .views import (
    applications,
    application_detail,
    payments,
    payment_detail,
    admission_letter,
    application_tracking,
    secure_application_tracking,
)


urlpatterns = [

    # ==============================
    # APPLICATIONS
    # ==============================

    path(
        'applications/',
        applications,
        name='applications'
    ),

    # IMPORTANT:
    # Keep the specific "track/" route
    # BEFORE <application_number>/

    path(
        'applications/track/',
        secure_application_tracking,
        name='secure-application-tracking'
    ),

    path(
        'applications/<str:application_number>/',
        application_detail,
        name='application-detail'
    ),

    path(
        'applications/<str:application_number>/track/',
        application_tracking,
        name='application-tracking'
    ),

    # ==============================
    # ADMISSION LETTER
    # ==============================

    path(
        'applications/<str:application_number>/admission-letter/',
        admission_letter,
        name='admission-letter'
    ),

    # ==============================
    # PAYMENTS
    # ==============================

    path(
        'payments/',
        payments,
        name='payments'
    ),

    path(
        'payments/<int:payment_id>/',
        payment_detail,
        name='payment-detail'
    ),

]