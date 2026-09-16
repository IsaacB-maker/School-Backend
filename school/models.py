from django.db import models


# =========================================================
# SCHOOL SETTINGS
# =========================================================

class SchoolSettings(models.Model):
    school_name = models.CharField(max_length=200)
    logo = models.ImageField(
        upload_to='school/',
        blank=True,
        null=True
    )

    hero_title = models.CharField(
        max_length=250,
        blank=True
    )

    hero_subtitle = models.CharField(
        max_length=250,
        blank=True
    )

    hero_description = models.TextField(
        blank=True
    )

    hero_image = models.ImageField(
        upload_to='school/hero/',
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=300,
        blank=True
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    vision = models.TextField(
        blank=True
    )

    mission = models.TextField(
        blank=True
    )

    welcome_message = models.TextField(
        blank=True
    )

    facebook = models.URLField(
        blank=True
    )

    instagram = models.URLField(
        blank=True
    )

    youtube = models.URLField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.school_name


# =========================================================
# NEWS
# =========================================================

class News(models.Model):
    title = models.CharField(max_length=250)

    image = models.ImageField(
        upload_to='news/',
        blank=True,
        null=True
    )

    content = models.TextField()

    published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


# =========================================================
# EVENTS
# =========================================================

class Event(models.Model):
    title = models.CharField(max_length=250)

    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True
    )

    description = models.TextField()

    date = models.DateField()

    time = models.TimeField(
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=250,
        blank=True
    )

    published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


# =========================================================
# GALLERY
# =========================================================

class Gallery(models.Model):
    title = models.CharField(
        max_length=200,
        blank=True
    )

    image = models.ImageField(
        upload_to="gallery/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or "Gallery Image"


# =========================================================
# STAFF
# =========================================================

class Staff(models.Model):
    name = models.CharField(
        max_length=200
    )

    position = models.CharField(
        max_length=200
    )

    department = models.CharField(
        max_length=200,
        blank=True
    )

    photo = models.ImageField(
        upload_to='staff/',
        blank=True,
        null=True
    )

    biography = models.TextField(
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=50,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.position}"


# =========================================================
# CONTACT SETTINGS
# =========================================================

class ContactSettings(models.Model):

    title = models.CharField(
        max_length=200,
        default="Contact Us"
    )

    introduction = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # CONTACT INFORMATION
    # -----------------------------------------------------

    address = models.TextField(
        blank=True,
        default=""
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    alternative_phone = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    email = models.EmailField(
        blank=True,
        default=""
    )

    alternative_email = models.EmailField(
        blank=True,
        default=""
    )

    whatsapp = models.CharField(
        max_length=50,
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # SCHOOL HOURS
    # -----------------------------------------------------

    monday_hours = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    tuesday_hours = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    wednesday_hours = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    thursday_hours = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    friday_hours = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    saturday_hours = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    sunday_hours = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------

    map_url = models.URLField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # SOCIAL MEDIA
    # -----------------------------------------------------

    facebook = models.URLField(
        blank=True,
        default=""
    )

    instagram = models.URLField(
        blank=True,
        default=""
    )

    youtube = models.URLField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    is_active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Contact Settings"
        verbose_name_plural = "Contact Settings"


# =========================================================
# ABOUT SCHOOL
# =========================================================

class AboutSchool(models.Model):

    # -----------------------------------------------------
    # HERO SECTION
    # -----------------------------------------------------

    hero_title = models.CharField(
        max_length=250,
        default="ABOUT PARACLETE"
    )

    hero_subtitle = models.CharField(
        max_length=300,
        default="More Than a School. A Foundation for Life."
    )

    hero_image = models.ImageField(
        upload_to='about/hero/',
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # WHO WE ARE
    # -----------------------------------------------------

    about_title = models.CharField(
        max_length=250,
        default="Who We Are"
    )

    about_description = models.TextField(
        blank=True,
        default=""
    )

    about_image = models.ImageField(
        upload_to='about/',
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # VISION
    # -----------------------------------------------------

    vision_title = models.CharField(
        max_length=200,
        default="Our Vision"
    )

    vision = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # MISSION
    # -----------------------------------------------------

    mission_title = models.CharField(
        max_length=200,
        default="Our Mission"
    )

    mission = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # SCHOOL LEADERSHIP MESSAGE
    # -----------------------------------------------------

    principal_title = models.CharField(
        max_length=200,
        default="A Message From Our School"
    )

    principal_message = models.TextField(
        blank=True,
        default=""
    )

    principal_name = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    principal_position = models.CharField(
        max_length=200,
        blank=True,
        default="School Principal"
    )

    principal_image = models.ImageField(
        upload_to='about/principal/',
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # EDUCATIONAL APPROACH
    # -----------------------------------------------------

    approach_title = models.CharField(
        max_length=250,
        default="Our Educational Approach"
    )

    approach_description = models.TextField(
        blank=True,
        default=""
    )

    # -----------------------------------------------------
    # CTA
    # -----------------------------------------------------

    cta_title = models.CharField(
        max_length=250,
        default="Your Child's Journey Starts Here"
    )

    cta_description = models.TextField(
        blank=True,
        default=""
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.hero_title

    class Meta:
        verbose_name = "About School"
        verbose_name_plural = "About School"


# =========================================================
# CORE VALUES
# =========================================================

class CoreValue(models.Model):

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon name or icon class."
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"

    def __str__(self):
        return self.title


# =========================================================
# WHY CHOOSE US
# =========================================================

class WhyChooseUs(models.Model):

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon name or icon class."
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Why Choose Us"
        verbose_name_plural = "Why Choose Us"

    def __str__(self):
        return self.title

    # ============================================================
# ACADEMIC PAGE
# ============================================================

class AcademicPage(models.Model):
    """
    Main content for the school's Academic page.
    Only one AcademicPage record should normally be created.
    """

    # --------------------------------------------------------
    # HERO SECTION
    # --------------------------------------------------------
    hero_title = models.CharField(
        max_length=200,
        default="Academic Excellence at Paraclete"
    )

    hero_subtitle = models.CharField(
        max_length=300,
        default="Building Knowledge, Character and a Future of Excellence."
    )

    hero_description = models.TextField(
        blank=True
    )

    hero_image = models.ImageField(
        upload_to="academic/",
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # CURRICULUM SECTION
    # --------------------------------------------------------
    curriculum_title = models.CharField(
        max_length=200,
        default="Our Curriculum"
    )

    curriculum_description = models.TextField(
        blank=True
    )

    curriculum_image = models.ImageField(
        upload_to="academic/",
        blank=True,
        null=True
    )

    # --------------------------------------------------------
    # TEACHING APPROACH INTRODUCTION
    # --------------------------------------------------------
    teaching_title = models.CharField(
        max_length=200,
        default="Our Teaching Approach"
    )

    teaching_description = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # ASSESSMENT INTRODUCTION
    # --------------------------------------------------------
    assessment_title = models.CharField(
        max_length=200,
        default="Assessment & Academic Progress"
    )

    assessment_description = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # ACADEMIC SUPPORT INTRODUCTION
    # --------------------------------------------------------
    support_title = models.CharField(
        max_length=200,
        default="Academic Support"
    )

    support_description = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # BEYOND THE CLASSROOM
    # --------------------------------------------------------
    beyond_classroom_title = models.CharField(
        max_length=200,
        default="Learning Beyond the Classroom"
    )

    beyond_classroom_description = models.TextField(
        blank=True
    )

    # --------------------------------------------------------
    # CTA SECTION
    # --------------------------------------------------------
    cta_title = models.CharField(
        max_length=200,
        default="Give Your Child the Foundation to Excel"
    )

    cta_description = models.TextField(
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Academic Page"
        verbose_name_plural = "Academic Page"

    def __str__(self):
        return self.hero_title


# ============================================================
# ACADEMIC LEVELS
# ============================================================

class AcademicLevel(models.Model):
    """
    Academic sections offered by the school.
    Example: Nursery, Primary, Secondary.
    """

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="academic/levels/",
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Academic Level"
        verbose_name_plural = "Academic Levels"

    def __str__(self):
        return self.title


# ============================================================
# ACADEMIC SUBJECTS
# ============================================================

class AcademicSubject(models.Model):
    """
    Subjects taught at the school.
    """

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon or emoji, e.g. 📐 or 🧪"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Academic Subject"
        verbose_name_plural = "Academic Subjects"

    def __str__(self):
        return self.title


# ============================================================
# TEACHING APPROACH
# ============================================================

class TeachingApproach(models.Model):
    """
    Individual teaching approaches used by the school.
    """

    title = models.CharField(
        max_length=150
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon or emoji"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Teaching Approach"
        verbose_name_plural = "Teaching Approaches"

    def __str__(self):
        return self.title


# ============================================================
# ACADEMIC SUPPORT
# ============================================================

class AcademicSupport(models.Model):
    """
    Academic support services offered to learners.
    """

    title = models.CharField(
        max_length=150
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon or emoji"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Academic Support"
        verbose_name_plural = "Academic Support"

    def __str__(self):
        return self.title


# ============================================================
# ACADEMIC ASSESSMENTS
# ============================================================

class AcademicAssessment(models.Model):
    """
    Different ways the school monitors learner progress.
    """

    title = models.CharField(
        max_length=150
    )

    description = models.TextField()

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon or emoji"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Academic Assessment"
        verbose_name_plural = "Academic Assessments"

    def __str__(self):
        return self.title