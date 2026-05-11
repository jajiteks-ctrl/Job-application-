
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    # -----------------------------
    # Choices
    # -----------------------------
    class JobType(models.TextChoices):
        FULL_TIME = "FULL_TIME", "Full Time"
        PART_TIME = "PART_TIME", "Part Time"
        CONTRACT = "CONTRACT", "Contract"
        INTERNSHIP = "INTERNSHIP", "Internship"
        FREELANCE = "FREELANCE", "Freelance"

    class WorkMode(models.TextChoices):
        ONSITE = "ONSITE", "On Site"
        REMOTE = "REMOTE", "Remote"
        HYBRID = "HYBRID", "Hybrid"

    class ExperienceLevel(models.TextChoices):
        FRESHER = "FRESHER", "Fresher"
        JUNIOR = "JUNIOR", "Junior"
        MID = "MID", "Mid Level"
        SENIOR = "SENIOR", "Senior"
        LEAD = "LEAD", "Lead"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"
        EXPIRED = "EXPIRED", "Expired"

    # -----------------------------
    # Basic Details
    # -----------------------------
    title = models.CharField(max_length=255)

    company_name = models.CharField(max_length=255)

    company_website = models.URLField(
        blank=True,
        null=True
    )

    company_logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    # -----------------------------
    # Job Details
    # -----------------------------
    description = models.TextField()

    responsibilities = models.TextField(
        blank=True,
        null=True
    )

    requirements = models.TextField(
        blank=True,
        null=True
    )

    skills_required = models.TextField(
        help_text="Comma separated skills"
    )

    qualification = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices
    )

    experience_min_years = models.PositiveIntegerField(
        default=0
    )

    experience_max_years = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    # -----------------------------
    # Job Type
    # -----------------------------
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices
    )

    work_mode = models.CharField(
        max_length=20,
        choices=WorkMode.choices
    )

    # -----------------------------
    # Salary
    # -----------------------------
    salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    salary_currency = models.CharField(
        max_length=10,
        default="INR"
    )

    salary_is_negotiable = models.BooleanField(
        default=False
    )

    # -----------------------------
    # Location
    # -----------------------------
    country = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    city = models.CharField(max_length=100)

    address = models.TextField(
        blank=True,
        null=True
    )

    # -----------------------------
    # Hiring Info
    # -----------------------------
    vacancies = models.PositiveIntegerField(default=1)

    application_deadline = models.DateField()

    joining_date = models.DateField(
        blank=True,
        null=True
    )

    # -----------------------------
    # Contact Info
    # -----------------------------
    hr_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    hr_email = models.EmailField(
        blank=True,
        null=True
    )

    hr_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # -----------------------------
    # SEO / Extra
    # -----------------------------
    benefits = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    is_featured = models.BooleanField(default=False)

    views_count = models.PositiveIntegerField(default=0)

    # -----------------------------
    # Admin Tracking
    # -----------------------------
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="jobs",
        limit_choices_to={"is_staff": True}
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------------
    # Meta
    # -----------------------------
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["city"]),
            models.Index(fields=["status"]),
            models.Index(fields=["job_type"]),
        ]

    # -----------------------------
    # String
    # -----------------------------
    def __str__(self):
        return f"{self.title} - {self.company_name}"
    
    
    
# =========================================================
# Job Application Model
# =========================================================

class JobApplication(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("SHORTLISTED", "Shortlisted"),
        ("REJECTED", "Rejected"),
        ("HIRED", "Hired"),
    )

    # -----------------------------------
    # Job + Candidate
    # -----------------------------------

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applied_jobs"
    )

    # -----------------------------------
    # Candidate Details
    # -----------------------------------

    full_name = models.CharField(max_length=255)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    resume = models.FileField(
        upload_to="resumes/"
    )

    cover_letter = models.TextField(
        blank=True,
        null=True
    )

    experience_years = models.PositiveIntegerField(
        default=0
    )

    current_company = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    current_ctc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    expected_ctc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    linkedin_url = models.URLField(
        blank=True,
        null=True
    )

    portfolio_url = models.URLField(
        blank=True,
        null=True
    )

    # -----------------------------------
    # Admin Tracking
    # -----------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    # -----------------------------------
    # Prevent Duplicate Apply
    # -----------------------------------

    class Meta:

        unique_together = ("job", "candidate")

        ordering = ["-applied_at"]

    def __str__(self):

        return f"{self.candidate.username} -> {self.job.title}"