from rest_framework import serializers
from .models import Application, Payment


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application

        fields = [
            'application_number',

            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'class_applying_for',
            'previous_school',

            'parent_name',
            'relationship',
            'parent_phone',
            'parent_email',
            'parent_address',

            'student_photo',
            'report_card',
            'birth_certificate',
            'additional_document',

            'status',
            'payment_status',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'application_number',
            'status',
            'payment_status',
            'created_at',
            'updated_at',
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment

        fields = '__all__'

        read_only_fields = [
            'id',
            'status',
            'created_at',
            'paid_at',
        ]