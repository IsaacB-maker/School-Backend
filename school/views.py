from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import (
    SchoolSettings,
    News,
    Event,
    Gallery,
    Staff,
    ContactSettings,
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

from .serializers import (
    SchoolSettingsSerializer,
    NewsSerializer,
    EventSerializer,
    GallerySerializer,
    StaffSerializer,
    ContactSettingsSerializer,
    AboutSchoolSerializer,
    CoreValueSerializer,
    WhyChooseUsSerializer,
    AcademicPageSerializer,
    AcademicLevelSerializer,
    AcademicSubjectSerializer,
    TeachingApproachSerializer,
    AcademicSupportSerializer,
    AcademicAssessmentSerializer,
)


# =========================================================
# CONTACT SETTINGS
# =========================================================

@api_view(["GET"])
def contact_settings(request):

    contact = ContactSettings.objects.filter(
        is_active=True
    ).first()

    if not contact:

        return Response(
            {
                "detail": "Contact information is not available."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ContactSettingsSerializer(
        contact
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


# =========================================================
# SCHOOL SETTINGS
# =========================================================

@api_view(['GET'])
def school_settings(request):

    settings = SchoolSettings.objects.first()

    if not settings:

        return Response(
            {
                "message": "School settings have not been created yet."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = SchoolSettingsSerializer(
        settings,
        context={'request': request}
    )

    return Response(
        serializer.data
    )


# =========================================================
# NEWS
# =========================================================

@api_view(['GET'])
def news_list(request):

    news = News.objects.filter(
        published=True
    )

    serializer = NewsSerializer(
        news,
        many=True,
        context={'request': request}
    )

    return Response(
        serializer.data
    )


# =========================================================
# EVENTS
# =========================================================

@api_view(['GET'])
def events_list(request):

    events = Event.objects.filter(
        published=True
    )

    serializer = EventSerializer(
        events,
        many=True,
        context={'request': request}
    )

    return Response(
        serializer.data
    )


# =========================================================
# GALLERY LIST
# =========================================================

@api_view(['GET'])
def gallery_list(request):

    gallery = Gallery.objects.all()

    serializer = GallerySerializer(
        gallery,
        many=True,
        context={'request': request}
    )

    return Response(
        serializer.data
    )


# =========================================================
# GALLERY DETAIL
# =========================================================

@api_view([
    'GET',
    'PUT',
    'PATCH',
    'DELETE'
])
def gallery_detail(request, pk):

    gallery = get_object_or_404(
        Gallery,
        pk=pk
    )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == 'GET':

        serializer = GallerySerializer(
            gallery,
            context={'request': request}
        )

        return Response(
            serializer.data
        )

    # -----------------------------------------------------
    # PUT / PATCH
    # -----------------------------------------------------

    if request.method in ['PUT', 'PATCH']:

        serializer = GallerySerializer(
            gallery,
            data=request.data,
            partial=(
                request.method == 'PATCH'
            ),
            context={'request': request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

    if request.method == 'DELETE':

        gallery.delete()

        return Response(
            {
                "message": "Gallery item deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )


# =========================================================
# STAFF
# =========================================================

@api_view(['GET'])
def staff_list(request):

    staff = Staff.objects.filter(
        is_active=True
    )

    serializer = StaffSerializer(
        staff,
        many=True,
        context={'request': request}
    )

    return Response(
        serializer.data
    )


# =========================================================
# ABOUT SCHOOL
# =========================================================

@api_view(['GET'])
def about_school(request):

    about = AboutSchool.objects.first()

    if not about:

        return Response(
            {
                "detail": "About School information is not available."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = AboutSchoolSerializer(
        about,
        context={'request': request}
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


# =========================================================
# CORE VALUES
# =========================================================

@api_view(['GET'])
def core_values(request):

    values = CoreValue.objects.filter(
        is_active=True
    )

    serializer = CoreValueSerializer(
        values,
        many=True,
        context={'request': request}
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


# =========================================================
# WHY CHOOSE US
# =========================================================

@api_view(['GET'])
def why_choose_us(request):

    items = WhyChooseUs.objects.filter(
        is_active=True
    )

    serializer = WhyChooseUsSerializer(
        items,
        many=True,
        context={'request': request}
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )

# ============================================================
# ACADEMIC API VIEWS
# ============================================================

@api_view(["GET"])
def academic_page(request):
    """
    Returns the main Academic page information.
    """

    academic = AcademicPage.objects.first()

    if not academic:
        return Response(
            {
                "detail": "Academic page information is not available."
            },
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = AcademicPageSerializer(
        academic,
        context={"request": request}
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def academic_levels(request):
    """
    Returns all active academic levels.
    """

    levels = AcademicLevel.objects.filter(
        is_active=True
    )

    serializer = AcademicLevelSerializer(
        levels,
        many=True,
        context={"request": request}
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def academic_subjects(request):
    """
    Returns all active academic subjects.
    """

    subjects = AcademicSubject.objects.filter(
        is_active=True
    )

    serializer = AcademicSubjectSerializer(
        subjects,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def teaching_approaches(request):
    """
    Returns all active teaching approaches.
    """

    approaches = TeachingApproach.objects.filter(
        is_active=True
    )

    serializer = TeachingApproachSerializer(
        approaches,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def academic_support(request):
    """
    Returns all active academic support services.
    """

    support = AcademicSupport.objects.filter(
        is_active=True
    )

    serializer = AcademicSupportSerializer(
        support,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def academic_assessments(request):
    """
    Returns all active academic assessment methods.
    """

    assessments = AcademicAssessment.objects.filter(
        is_active=True
    )

    serializer = AcademicAssessmentSerializer(
        assessments,
        many=True
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )