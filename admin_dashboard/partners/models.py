from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    website = models.URLField(blank=True)
    contact_email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='partners/logos/', blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Affiliate(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='affiliates')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    contact_email = models.EmailField(blank=True)
    logo = models.ImageField(upload_to='partners/affiliates/logos/', blank=True)
    description = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Affiliate'
        verbose_name_plural = 'Affiliates'
        unique_together = ('partner', 'slug')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.name} ({self.partner.name})"
