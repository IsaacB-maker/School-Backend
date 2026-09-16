import re
from .services.admission_letter import generate_admission_letter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Application, Payment
from .serializers import (
    ApplicationSerializer,
    PaymentSerializer
)


# ==================================================
# APPLICATIONS
# ==================================================

@api_view(['POST'])
def applications(request):

    serializer = ApplicationSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():

        application = serializer.save()

        return Response(
            ApplicationSerializer(
                application,
                context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
def application_detail(request, application_number):

    return Response(
        {
            'success': False,
            'message': (
                'Direct application details are not '
                'available through the public API. '
                'Please use the secure tracking endpoint.'
            )
        },
        status=status.HTTP_403_FORBIDDEN
    )

# ==================================================
# PAYMENTS
# ==================================================

@api_view(['GET', 'POST'])
def payments(request):

    # GET ALL PAYMENTS
    if request.method == 'GET':

        payments = Payment.objects.all()

        serializer = PaymentSerializer(
            payments,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    # CREATE PAYMENT
    if request.method == 'POST':

        serializer = PaymentSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():

            payment = serializer.save()

            return Response(
                PaymentSerializer(
                    payment,
                    context={'request': request}
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==================================================
# SINGLE PAYMENT
# ==================================================

@api_view(['GET'])
def payment_detail(request, payment_id):

    try:

        payment = Payment.objects.get(
            id=payment_id
        )

    except Payment.DoesNotExist:

        return Response(
            {
                'message': 'Payment not found.'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = PaymentSerializer(
        payment,
        context={'request': request}
    )

    return Response(serializer.data)
@api_view(['GET'])
def admission_letter(request, application_number):

    try:

        application = Application.objects.get(
            application_number=application_number
        )

    except Application.DoesNotExist:

        return Response(
            {
                'success': False,
                'message': 'Application not found.'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # ==========================================
    # CHECK APPLICATION APPROVAL
    # ==========================================

    if application.status != 'Approved':

        return Response(
            {
                'success': False,
                'message': (
                    'Admission letter is only available '
                    'after the application has been approved.'
                )
            },
            status=status.HTTP_403_FORBIDDEN
        )

    # ==========================================
    # CHECK PAYMENT CONFIRMATION
    # ==========================================

    if application.payment_status != 'Paid':

        return Response(
            {
                'success': False,
                'message': (
                    'Admission letter is only available '
                    'after the admission payment has been confirmed.'
                )
            },
            status=status.HTTP_403_FORBIDDEN
        )

    # ==========================================
    # BOTH CONDITIONS PASSED
    # ==========================================

    return generate_admission_letter(application)
@api_view(['GET'])
def application_tracking(request, application_number):

    try:
        application = Application.objects.get(
            application_number=application_number
        )

    except Application.DoesNotExist:

        return Response(
            {
                'success': False,
                'message': 'Application not found.'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        {
            'success': True,

            'application': {
                'application_number':
                    application.application_number,

                'student_name':
                    f"{application.first_name} "
                    f"{application.last_name}",

                'class_applying_for':
                    application.class_applying_for,

                'application_status':
                    application.status,

                'payment_status':
                    application.payment_status,

                'submitted_at':
                    application.created_at,

                'updated_at':
                    application.updated_at,
            }
        },
        status=status.HTTP_200_OK
    )

def normalize_phone(phone):
    """
    Convert Ugandan phone numbers to one standard format.

    Examples:
    0700123456     -> 256700123456
    +256700123456  -> 256700123456
    256700123456   -> 256700123456
    """

    if not phone:
        return ""

    # Remove spaces, hyphens and other characters
    phone = re.sub(r'\D', '', phone)

    # 0700xxxxxx -> 256700xxxxxx
    if phone.startswith('0'):
        phone = '256' + phone[1:]

    # +256 is already removed by the regex
    elif phone.startswith('256'):
        phone = phone

    return phone

@api_view(['POST'])
def secure_application_tracking(request):

    application_number = request.data.get(
        'application_number'
    )

    parent_phone = request.data.get(
        'parent_phone'
    )

    # ==========================================
    # CHECK REQUIRED FIELDS
    # ==========================================

    if not application_number or not parent_phone:

        return Response(
            {
                'success': False,
                'message': (
                    'Application number and '
                    'parent phone are required.'
                )
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ==========================================
    # FIND APPLICATION
    # ==========================================

    try:

        application = Application.objects.get(
            application_number=application_number
        )

    except Application.DoesNotExist:

        return Response(
            {
                'success': False,
                'message': 'Application not found.'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # ==========================================
    # NORMALIZE PHONE NUMBERS
    # ==========================================

    stored_phone = normalize_phone(
        application.parent_phone
    )

    submitted_phone = normalize_phone(
        parent_phone
    )

    # ==========================================
    # VERIFY PHONE
    # ==========================================

    if stored_phone != submitted_phone:

        return Response(
            {
                'success': False,
                'message': (
                    'The application number or '
                    'phone number is incorrect.'
                )
            },
            status=status.HTTP_403_FORBIDDEN
        )

    # ==========================================
    # RETURN SAFE INFORMATION
    # ==========================================

    return Response(
        {
            'success': True,

            'application': {

                'application_number':
                    application.application_number,

                'student_name':
                    f"{application.first_name} "
                    f"{application.last_name}",

                'class_applying_for':
                    application.class_applying_for,

                'application_status':
                    application.status,

                'payment_status':
                    application.payment_status,

                'submitted_at':
                    application.created_at,

                'updated_at':
                    application.updated_at,
            }
        },
        status=status.HTTP_200_OK
    )