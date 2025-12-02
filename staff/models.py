from django.db import models


class StaffMember(models.Model):
    full_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)

    def __str__(self):
        return self.full_name
