from django.db import models
from django.conf import settings


class StaffMember(models.Model):
    full_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)

    def __str__(self):
        return self.full_name


class Leadership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, help_text='Optional linked user account for leader login')
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='leadership_photos/', null=True, blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Leadership'
        verbose_name_plural = 'Leaderships'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} — {self.position}"
