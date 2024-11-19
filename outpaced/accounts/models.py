from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Extends the default Django User model with additional fields.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signals to create or update UserProfile automatically

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates or updates the UserProfile whenever the User instance is created or saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()