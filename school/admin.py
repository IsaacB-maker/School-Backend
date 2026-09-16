from django.contrib import admin

from .models import (
    SchoolSettings,
    ContactSettings,
    News,
    Event,
    Gallery,
    Staff,
    AboutSchool,
    CoreValue,
    WhyChooseUs,
    AcademicPage,
    AcademicLevel,
    AcademicSubject,
    TeachingApproach,
    AcademicSupport,
    AcademicAssessment,
)


# =========================================================
# SCHOOL SETTINGS ADMIN
# =========================================================

@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):

    list_display = (
        'school_name',
        'phone',
        'email',
        'updated_at',
    )


# =========================================================
# CONTACT SETTINGS ADMIN
# =========================================================

@admin.register(ContactSettings)
class ContactSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "phone",
        "email",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
        "address",
        "phone",
        "email",
    )

    readonly_fields = (
        "updated_at",
    )

    fieldsets = (

        (
            "Contact Page",
            {
                "fields": (
                    "title",
                    "introduction",
                )
            }
        ),

        (
            "Contact Information",
            {
                "fields": (
                    "address",
                    "phone",
                    "alternative_phone",
                    "email",
                    "alternative_email",
                    "whatsapp",
                )
            }
        ),

        (
            "School Hours",
            {
                "fields": (
                    "monday_hours",
                    "tuesday_hours",
                    "wednesday_hours",
                    "thursday_hours",
                    "friday_hours",
                    "saturday_hours",
                    "sunday_hours",
                )
            }
        ),

        (
            "Map",
            {
                "fields": (
                    "map_url",
                )
            }
        ),

        (
            "Social Media",
            {
                "fields": (
                    "facebook",
                    "instagram",
                    "youtube",
                )
            }
        ),

        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "updated_at",
                )
            }
        ),

    )


# =========================================================
# NEWS ADMIN
# =========================================================

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'published',
        'created_at',
    )

    list_filter = (
        'published',
        'created_at',
    )

    search_fields = (
        'title',
        'content',
    )


# =========================================================
# EVENTS ADMIN
# =========================================================

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'date',
        'time',
        'location',
        'published',
    )

    list_filter = (
        'published',
        'date',
    )

    search_fields = (
        'title',
        'location',
    )


# =========================================================
# GALLERY ADMIN
# =========================================================

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
    )


# =========================================================
# STAFF ADMIN
# =========================================================

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'position',
        'department',
        'is_active',
    )

    list_filter = (
        'is_active',
        'department',
    )

    search_fields = (
        'name',
        'position',
        'department',
    )


# =========================================================
# ABOUT SCHOOL ADMIN
# =========================================================

@admin.register(AboutSchool)
class AboutSchoolAdmin(admin.ModelAdmin):

    list_display = (
        'hero_title',
        'principal_name',
        'updated_at',
    )

    search_fields = (
        'hero_title',
        'hero_subtitle',
        'about_title',
        'principal_name',
    )

    readonly_fields = (
        'updated_at',
    )

    fieldsets = (

        # -------------------------------------------------
        # HERO
        # -------------------------------------------------

        (
            "About Page Hero",
            {
                "fields": (
                    "hero_title",
                    "hero_subtitle",
                    "hero_image",
                )
            }
        ),

        # -------------------------------------------------
        # WHO WE ARE
        # -------------------------------------------------

        (
            "Who We Are",
            {
                "fields": (
                    "about_title",
                    "about_description",
                    "about_image",
                )
            }
        ),

        # -------------------------------------------------
        # VISION
        # -------------------------------------------------

        (
            "Our Vision",
            {
                "fields": (
                    "vision_title",
                    "vision",
                )
            }
        ),

        # -------------------------------------------------
        # MISSION
        # -------------------------------------------------

        (
            "Our Mission",
            {
                "fields": (
                    "mission_title",
                    "mission",
                )
            }
        ),

        # -------------------------------------------------
        # SCHOOL LEADERSHIP
        # -------------------------------------------------

        (
            "School Leadership Message",
            {
                "fields": (
                    "principal_title",
                    "principal_message",
                    "principal_name",
                    "principal_position",
                    "principal_image",
                )
            }
        ),

        # -------------------------------------------------
        # EDUCATIONAL APPROACH
        # -------------------------------------------------

        (
            "Educational Approach",
            {
                "fields": (
                    "approach_title",
                    "approach_description",
                )
            }
        ),

        # -------------------------------------------------
        # CALL TO ACTION
        # -------------------------------------------------

        (
            "Final Call To Action",
            {
                "fields": (
                    "cta_title",
                    "cta_description",
                )
            }
        ),

        # -------------------------------------------------
        # SYSTEM
        # -------------------------------------------------

        (
            "System Information",
            {
                "fields": (
                    "updated_at",
                )
            }
        ),
    )


# =========================================================
# CORE VALUES ADMIN
# =========================================================

@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'order',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'title',
        'description',
    )

    list_editable = (
        'order',
        'is_active',
    )

    ordering = (
        'order',
        'title',
    )


# =========================================================
# WHY CHOOSE US ADMIN
# =========================================================

@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'order',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'title',
        'description',
    )

    list_editable = (
        'order',
        'is_active',
    )

    ordering = (
        'order',
        'title',
    )

    # ============================================================
# ACADEMIC ADMIN
# ============================================================

@admin.register(AcademicPage)
class AcademicPageAdmin(admin.ModelAdmin):
    list_display = (
        "hero_title",
        "hero_subtitle",
        "updated_at",
    )

    readonly_fields = (
        "updated_at",
    )

    fieldsets = (
        (
            "Hero Section",
            {
                "fields": (
                    "hero_title",
                    "hero_subtitle",
                    "hero_description",
                    "hero_image",
                )
            },
        ),
        (
            "Curriculum",
            {
                "fields": (
                    "curriculum_title",
                    "curriculum_description",
                    "curriculum_image",
                )
            },
        ),
        (
            "Teaching Approach",
            {
                "fields": (
                    "teaching_title",
                    "teaching_description",
                )
            },
        ),
        (
            "Assessment",
            {
                "fields": (
                    "assessment_title",
                    "assessment_description",
                )
            },
        ),
        (
            "Academic Support",
            {
                "fields": (
                    "support_title",
                    "support_description",
                )
            },
        ),
        (
            "Beyond the Classroom",
            {
                "fields": (
                    "beyond_classroom_title",
                    "beyond_classroom_description",
                )
            },
        ),
        (
            "Call To Action",
            {
                "fields": (
                    "cta_title",
                    "cta_description",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "updated_at",
                )
            },
        ),
    )


@admin.register(AcademicLevel)
class AcademicLevelAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(AcademicSubject)
class AcademicSubjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "icon",
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(TeachingApproach)
class TeachingApproachAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "icon",
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(AcademicSupport)
class AcademicSupportAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "icon",
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )


@admin.register(AcademicAssessment)
class AcademicAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "icon",
        "order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "order",
        "is_active",
    )

    search_fields = (
        "title",
        "description",
    )