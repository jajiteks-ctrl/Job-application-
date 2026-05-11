# serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, Job


# =========================================================
# Register Serializer
# =========================================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        ]

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)

        Profile.objects.create(user=user)

        return user


# =========================================================
# Profile Serializer
# =========================================================

class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.CharField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = Profile

        fields = [
            "id",
            'username',
            'email',
            'phone',
            'address'
        ]


# =========================================================
# Bulk Job Serializer
# =========================================================

class BulkJobListSerializer(serializers.ListSerializer):

    def create(self, validated_data):

        user = self.context["request"].user

        jobs = []

        for item in validated_data:

            item["created_by"] = user

            jobs.append(Job(**item))

        return Job.objects.bulk_create(jobs)


# =========================================================
# Job Serializer
# =========================================================

class JobSerializer(serializers.ModelSerializer):

    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job

        fields = "__all__"

        read_only_fields = (
            "id",
            "created_by",
            "created_at",
            "updated_at",
            "views_count",
        )

        list_serializer_class = BulkJobListSerializer

    # -----------------------------------
    # Single Job Create
    # -----------------------------------

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        return super().create(validated_data)
    
    
    
# serializers.py

from .models import JobApplication


# =========================================================
# Job Application Serializer
# =========================================================

class JobApplicationSerializer(serializers.ModelSerializer):

    candidate = serializers.StringRelatedField(read_only=True)

    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    class Meta:

        model = JobApplication

        fields = "__all__"

        read_only_fields = (
            "candidate",
            "status",
            "applied_at",
        )

    # -----------------------------------
    # Auto Attach Candidate
    # -----------------------------------

    def create(self, validated_data):

        request = self.context.get("request")

        validated_data["candidate"] = request.user

        return super().create(validated_data)

    # -----------------------------------
    # Prevent Duplicate Applications
    # -----------------------------------

    def validate(self, data):

        user = self.context["request"].user

        job = data["job"]

        already_applied = JobApplication.objects.filter(
            candidate=user,
            job=job
        ).exists()

        if already_applied:

            raise serializers.ValidationError(
                "You already applied for this job."
            )

        return data