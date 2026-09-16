from django.urls import path

from .views import (
    school_settings,
    contact_settings,
    news_list,
    events_list,
    gallery_list,
    gallery_detail,
    staff_list,
    about_school,
    core_values,
    why_choose_us,
    academic_page,
    academic_levels,
    academic_subjects,
    teaching_approaches,
    academic_support,
    academic_assessments,
)


urlpatterns = [

    # =====================================================
    # CONTACT
    # =====================================================

    path(
        "contact/",
        contact_settings,
        name="contact-settings"
    ),

    # =====================================================
    # SCHOOL SETTINGS
    # =====================================================

    path(
        "settings/",
        school_settings,
        name="school-settings"
    ),

    # =====================================================
    # NEWS
    # =====================================================

    path(
        "news/",
        news_list,
        name="news-list"
    ),

    # =====================================================
    # EVENTS
    # =====================================================

    path(
        "events/",
        events_list,
        name="events-list"
    ),

    # =====================================================
    # GALLERY
    # =====================================================

    path(
        "gallery/",
        gallery_list,
        name="gallery-list"
    ),

    path(
        "gallery/<int:pk>/",
        gallery_detail,
        name="gallery-detail"
    ),

    # =====================================================
    # STAFF
    # =====================================================

    path(
        "staff/",
        staff_list,
        name="staff-list"
    ),

    # =====================================================
    # ABOUT SCHOOL
    # =====================================================

    path(
        "about/",
        about_school,
        name="about-school"
    ),

    # =====================================================
    # CORE VALUES
    # =====================================================

    path(
        "core-values/",
        core_values,
        name="core-values"
    ),

    # =====================================================
    # WHY CHOOSE US
    # =====================================================

    path(
        "why-choose-us/",
        why_choose_us,
        name="why-choose-us"
    ),

    # ============================================================
# ACADEMIC
# ============================================================

path(
    "academic/",
    academic_page,
    name="academic-page"
),

path(
    "academic/levels/",
    academic_levels,
    name="academic-levels"
),

path(
    "academic/subjects/",
    academic_subjects,
    name="academic-subjects"
),

path(
    "academic/approaches/",
    teaching_approaches,
    name="teaching-approaches"
),

path(
    "academic/support/",
    academic_support,
    name="academic-support"
),

path(
    "academic/assessments/",
    academic_assessments,
    name="academic-assessments"
),
]