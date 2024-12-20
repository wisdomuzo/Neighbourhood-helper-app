from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    CATEGORY_CHOICES = [
        ('moving', 'Moving'),
        ('babysitting', 'Babysitting'),
        ('repair', 'Repair'),
        ('shopping', 'Shopping'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    urgency = models.PositiveSmallIntegerField(help_text="Rate urgency from 1 (low) to 5 (high)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    required_skills = models.TextField(blank=True, null=True, help_text="List required skills, if any")
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# null=True added to required_skills to prevent database-level errors when blank fields are submitted.
# related_name='tasks' added to posted_by for easier querying of user-specific tasks.
# Default consistency checks for status and urgency

