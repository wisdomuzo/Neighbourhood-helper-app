from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    phone_no = models.CharField(max_length=13, null=False, default='')

    def __str__(self):
        return self.user.username

# The signal logic 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# User's ratings and reviews
class UserRating(models.Model):
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.IntegerField(default=1)
    review = models.TextField(blank=True)

    def __str__(self):
        return f"{self.rated_by} -> {self.rated_user}: {self.rating}"



# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# import uuid

# class Profile(models.Model):
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#         ('N', 'Prefer Not to Say')
#     ]

#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
#     # Personal Information
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
    
#     # Contact Information
#     phone_number = models.CharField(max_length=15, blank=True)
#     alternative_email = models.EmailField(blank=True)
    
#     # Profile Details
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=100, blank=True)
#     skills = models.TextField(blank=True, help_text="List your skills separated by commas")
    
#     # Profile Picture
#     profile_picture = models.ImageField(
#         upload_to='profile_pictures/', 
#         null=True, 
#         blank=True, 
#         max_length=255
#     )
    
#     # Professional Information
#     occupation = models.CharField(max_length=100, blank=True)
#     organization = models.CharField(max_length=100, blank=True)
    
#     # Account Preferences
#     is_volunteer = models.BooleanField(default=False)
#     is_service_provider = models.BooleanField(default=False)
    
#     # Ratings and Metrics
#     total_tasks_completed = models.IntegerField(default=0)
#     average_rating = models.FloatField(default=0.0)
#     reputation_score = models.IntegerField(default=100)
    
#     # Timestamps
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.user.email}'s Profile"
    
#     @property
#     def full_name(self):
#         return f"{self.first_name} {self.last_name}".strip()

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


