from rest_framework import serializers

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


# =========================================================
# CONTACT SETTINGS SERIALIZER
# =========================================================

class ContactSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactSettings
        fields = "__all__"


# =========================================================
# SCHOOL SETTINGS SERIALIZER
# =========================================================

class SchoolSettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolSettings
        fields = "__all__"


# =========================================================
# NEWS SERIALIZER
# =========================================================

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"


# =========================================================
# EVENTS SERIALIZER
# =========================================================

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"


# =========================================================
# GALLERY SERIALIZER
# =========================================================

class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery

        fields = [
            "id",
            "title",
            "image",
            "caption",
            "description",
            "created_at",
        ]


# =========================================================
# STAFF SERIALIZER
# =========================================================

class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = "__all__"


# =========================================================
# ABOUT SCHOOL SERIALIZER
# =========================================================

class AboutSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutSchool
        fields = "__all__"


# =========================================================
# CORE VALUES SERIALIZER
# =========================================================

class CoreValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoreValue
        fields = "__all__"


# =========================================================
# WHY CHOOSE US SERIALIZER
# =========================================================

class WhyChooseUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WhyChooseUs
        fields = "__all__"

# ============================================================
# ACADEMIC SERIALIZERS
# ============================================================

class AcademicPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicPage
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get("request")

        if request:
            if instance.hero_image:
                data["hero_image"] = request.build_absolute_uri(
                    instance.hero_image.url
                )

            if instance.curriculum_image:
                data["curriculum_image"] = request.build_absolute_uri(
                    instance.curriculum_image.url
                )

        return data


class AcademicLevelSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = AcademicLevel
        fields = [
            "id",
            "title",
            "description",
            "image",
            "order",
            "is_active",
        ]

    def get_image(self, obj):
        if not obj.image:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.image.url)

        return obj.image.url


class AcademicSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSubject
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "order",
            "is_active",
        ]


class TeachingApproachSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingApproach
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "order",
            "is_active",
        ]


class AcademicSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSupport
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "order",
            "is_active",
        ]


class AcademicAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicAssessment
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "order",
            "is_active",
        ]