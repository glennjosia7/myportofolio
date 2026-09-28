import uuid
from django.contrib.auth.models import User
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
        ('organization', 'Organization'),
        ('committee', 'Committee'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Achievement(models.Model):
    title = models.CharField(max_length=255)
    result = models.CharField(max_length=100)
    organizer = models.CharField(max_length=255)
    evidence_image = models.CharField(max_length=255, blank=True)
    # CV tidak selalu mencantumkan tahun, jadi field ini boleh kosong.
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.result} - {self.title}"


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True)
    project_image_url = models.URLField(blank=True, max_length=500)
    # Satu proyek bisa di-star banyak pengguna, dan sebaliknya.
    starred_by = models.ManyToManyField(
        User, related_name="starred_projects", blank=True
    )

    def __str__(self):
        return self.title


class Certification(models.Model):
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=255)
    credential_url = models.URLField()
    # Satu certification bisa di-star banyak pengguna, dan sebaliknya.
    starred_by = models.ManyToManyField(
        User, related_name="starred_certifications", blank=True
    )

    def __str__(self):
        return self.name
