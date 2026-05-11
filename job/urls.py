"""
URL configuration for job project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from app.views import RegisterView, ProfileView
from app.views import (
    JobListCreateView,
    JobDetailView,
    JobUpdateView,
    JobDeleteView,
)


from app.views import (
    ApplyJobView,
    MyApplicationsView,
    AllApplicationsView,
    JobApplicationsView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
     
    # 🔐 Auth
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 👤 Profile
    path('api/profile/', ProfileView.as_view(), name='profile'),
    
     path(
        "jobs/",
        JobListCreateView.as_view(),
        name="job-list-create"
    ),

    # Retrieve
    path(
        "jobs/<int:id>/",
        JobDetailView.as_view(),
        name="job-detail"
    ),

    # Update
    path(
        "jobs/<int:id>/update/",
        JobUpdateView.as_view(),
        name="job-update"
    ),

    # Delete
    path(
        "jobs/<int:id>/delete/",
        JobDeleteView.as_view(),
        name="job-delete"
    ),

 # =========================================================
    # Candidate Apply Job
    # =========================================================

    path(
        "jobs/apply/",
        ApplyJobView.as_view(),
        name="apply-job"
    ),

    # =========================================================
    # Candidate My Applications
    # =========================================================

    path(
        "my-applications/",
        MyApplicationsView.as_view(),
        name="my-applications"
    ),

    # =========================================================
    # Admin See All Applications
    # =========================================================

    path(
        "applications/",
        AllApplicationsView.as_view(),
        name="all-applications"
    ),

    # =========================================================
    # Admin See Applications Per Job
    # =========================================================

    path(
        "jobs/<int:job_id>/applications/",
        JobApplicationsView.as_view(),
        name="job-applications"
    ),
]


