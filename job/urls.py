"""
URL configuration for job project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.views import (
    RegisterView,
    ProfileView,

    JobListCreateView,
    JobDetailView,
    JobUpdateView,
    JobDeleteView,

    ApplyJobView,
    MyApplicationsView,
    AllApplicationsView,
    JobApplicationsView,
)


# =========================================================
# Home/Test API
# =========================================================

def home(request):
    return JsonResponse({
        "status": "success",
        "message": "Django backend deployed successfully on Render 🚀"
    })


# =========================================================
# URL Patterns
# =========================================================

urlpatterns = [

    # Home/Test URL
    path('', home),

    # Admin
    path('admin/', admin.site.urls),

    # =========================================================
    # Authentication
    # =========================================================

    path(
        'api/register/',
        RegisterView.as_view(),
        name='register'
    ),

    path(
        'api/login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # =========================================================
    # Profile
    # =========================================================

    path(
        'api/profile/',
        ProfileView.as_view(),
        name='profile'
    ),

    # =========================================================
    # Jobs
    # =========================================================

    path(
        "jobs/",
        JobListCreateView.as_view(),
        name="job-list-create"
    ),

    path(
        "jobs/<int:id>/",
        JobDetailView.as_view(),
        name="job-detail"
    ),

    path(
        "jobs/<int:id>/update/",
        JobUpdateView.as_view(),
        name="job-update"
    ),

    path(
        "jobs/<int:id>/delete/",
        JobDeleteView.as_view(),
        name="job-delete"
    ),

    # =========================================================
    # Applications
    # =========================================================

    path(
        "jobs/apply/",
        ApplyJobView.as_view(),
        name="apply-job"
    ),

    path(
        "my-applications/",
        MyApplicationsView.as_view(),
        name="my-applications"
    ),

    path(
        "applications/",
        AllApplicationsView.as_view(),
        name="all-applications"
    ),

    path(
        "jobs/<int:job_id>/applications/",
        JobApplicationsView.as_view(),
        name="job-applications"
    ),
]