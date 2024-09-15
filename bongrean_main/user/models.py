from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='static/images/profile_default_avatar.jpg', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        # Remove the UniqueConstraint as MySQL doesn't support it with conditions
        pass