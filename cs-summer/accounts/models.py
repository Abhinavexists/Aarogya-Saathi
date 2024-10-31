from django.db import models
from django.contrib.auth.hashers import make_password

class UserProfile(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store encrypted password

    def save(self, *args, **kwargs):
        # Encrypt password before saving
        if not self.pk:  # Only hash if it's a new record
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
