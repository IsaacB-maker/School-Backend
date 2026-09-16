from django.db import models


class Application(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    application_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    # =========================
    # STUDENT INFORMATION
    # =========================

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    class_applying_for = models.CharField(
        max_length=100
    )

    previous_school = models.CharField(
        max_length=200,
        blank=True
    )

    # =========================
    # PARENT / GUARDIAN
    # =========================

    parent_name = models.CharField(
        max_length=200
    )

    relationship = models.CharField(
        max_length=100
    )

    parent_phone = models.CharField(
        max_length=50
    )

    parent_email = models.EmailField(
        blank=True
    )

    parent_address = models.TextField(
        blank=True
    )

    # =========================
    # DOCUMENTS
    # =========================

    student_photo = models.ImageField(
        upload_to='applications/photos/',
        blank=True,
        null=True
    )

    report_card = models.FileField(
        upload_to='applications/reports/',
        blank=True,
        null=True
    )

    birth_certificate = models.FileField(
        upload_to='applications/birth_certificates/',
        blank=True,
        null=True
    )

    additional_document = models.FileField(
        upload_to='applications/additional/',
        blank=True,
        null=True
    )

    # =========================
    # APPLICATION MANAGEMENT
    # =========================

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================
    # APPLICATION NUMBER
    # =========================

    def save(self, *args, **kwargs):

        if not self.application_number:

            last_application = (
                Application.objects
                .order_by('-id')
                .first()
            )

            if last_application:
                number = last_application.id + 1
            else:
                number = 1

            self.application_number = (
                f"ADM-2026-{number:05d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.application_number} - "
            f"{self.first_name} {self.last_name}"
        )


# ==================================================
# PAYMENT
# ==================================================

class Payment(models.Model):

    PAYMENT_METHODS = [
        ('Mobile Money', 'Mobile Money'),
        ('Card', 'Card'),
        ('Bank', 'Bank'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS
    )

    reference = models.CharField(
        max_length=150,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        from django.utils import timezone

        # ==========================================
        # AUTOMATIC PAID TIMESTAMP
        # ==========================================

        if self.status == 'Paid' and not self.paid_at:

            self.paid_at = timezone.now()

        super().save(*args, **kwargs)

        # ==========================================
        # CALCULATE APPLICATION PAYMENT STATUS
        # ==========================================

        application = self.application

        payments = Payment.objects.filter(
            application=application
        )

        # ------------------------------------------
        # ANY PAID PAYMENT = PAID
        # ------------------------------------------

        if payments.filter(status='Paid').exists():

            new_status = 'Paid'

        # ------------------------------------------
        # NO PAID PAYMENT
        # ------------------------------------------

        elif payments.filter(status='Processing').exists():

            new_status = 'Processing'

        elif payments.filter(status='Pending').exists():

            new_status = 'Pending'

        elif payments.filter(status='Refunded').exists():

            new_status = 'Refunded'

        else:

            new_status = 'Failed'

        # ==========================================
        # UPDATE APPLICATION
        # ==========================================

        if application.payment_status != new_status:

            application.payment_status = new_status

            application.save(
                update_fields=[
                    'payment_status',
                    'updated_at'
                ]
            )

    def __str__(self):

        return (
            f"{self.application.application_number} - "
            f"{self.amount}"
        )