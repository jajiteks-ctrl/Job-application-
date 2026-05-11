# views.py

from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .models import Job
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    JobSerializer
)

from .permissions import IsAdminUserOnly


# =========================================================
# Register View
# =========================================================

from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# =========================================================
# Profile View
# =========================================================

class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):

        return self.request.user.profile


# =========================================================
# List All Jobs + Create Jobs (Single + Bulk)
# =========================================================

class JobListCreateView(generics.ListCreateAPIView):

    queryset = Job.objects.all()

    serializer_class = JobSerializer

    # -----------------------------------
    # Filters
    # -----------------------------------

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = [
        "job_type",
        "work_mode",
        "experience_level",
        "city",
        "state",
        "country",
        "status",
        "is_featured",
    ]

    search_fields = [
        "title",
        "company_name",
        "skills_required",
        "city",
    ]

    ordering_fields = [
        "created_at",
        "salary_min",
        "salary_max",
    ]

    # -----------------------------------
    # Permissions
    # -----------------------------------

    def get_permissions(self):

        # Only Admin can create jobs
        if self.request.method == "POST":
            return [IsAdminUserOnly()]

        # Only logged-in users can view jobs
        return [permissions.IsAuthenticated()]

    # -----------------------------------
    # Enable Bulk Create
    # -----------------------------------

    def get_serializer(self, *args, **kwargs):

        data = kwargs.get("data")

        if isinstance(data, list):
            kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)

    # -----------------------------------
    # Create Job
    # -----------------------------------

    def perform_create(self, serializer):

        serializer.save()
# =========================================================
# Retrieve Single Job
# =========================================================

class JobDetailView(generics.RetrieveAPIView):

    queryset = Job.objects.all()

    serializer_class = JobSerializer

    permission_classes = [permissions.IsAuthenticated]

    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        # Increase View Count
        instance.views_count += 1

        instance.save()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)


# =========================================================
# Update Job
# =========================================================

class JobUpdateView(generics.UpdateAPIView):

    queryset = Job.objects.all()

    serializer_class = JobSerializer

    permission_classes = [IsAdminUserOnly]

    lookup_field = "id"


# =========================================================
# Delete Job
# =========================================================

class JobDeleteView(generics.DestroyAPIView):

    queryset = Job.objects.all()

    serializer_class = JobSerializer

    permission_classes = [IsAdminUserOnly]

    lookup_field = "id"
    
    
# views.py

from .models import JobApplication
from .serializers import JobApplicationSerializer


# =========================================================
# Candidate Apply Job
# =========================================================

class ApplyJobView(generics.CreateAPIView):

    serializer_class = JobApplicationSerializer

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save()


# =========================================================
# Candidate My Applications
# =========================================================

class MyApplicationsView(generics.ListAPIView):

    serializer_class = JobApplicationSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return JobApplication.objects.filter(
            candidate=self.request.user
        )


# =========================================================
# Admin See All Applications
# =========================================================

class AllApplicationsView(generics.ListAPIView):

    serializer_class = JobApplicationSerializer

    permission_classes = [IsAdminUserOnly]

    queryset = JobApplication.objects.all()


# =========================================================
# Admin See Applications Per Job
# =========================================================

class JobApplicationsView(generics.ListAPIView):

    serializer_class = JobApplicationSerializer

    permission_classes = [IsAdminUserOnly]

    def get_queryset(self):

        job_id = self.kwargs["job_id"]

        return JobApplication.objects.filter(
            job_id=job_id
        )
        
