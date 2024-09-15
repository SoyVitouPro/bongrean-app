from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(max_length=200, blank=True, null=True)  # Changed to URLField
    email = models.EmailField(max_length=254, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

# Signal to create Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email=instance.email,
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.email = instance.email
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance, email=instance.email)