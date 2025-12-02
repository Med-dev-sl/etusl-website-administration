from django.db import models


class UniversityPolicy(models.Model):
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('hr', 'Human Resources'),
        ('finance', 'Finance'),
        ('governance', 'Governance'),
        ('student_affairs', 'Student Affairs'),
        ('health_safety', 'Health & Safety'),
        ('it', 'Information Technology'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    content = models.TextField()
    document = models.FileField(upload_to='policies/documents/', blank=True, help_text='PDF or Word document')
    published_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'University Policy'
        verbose_name_plural = 'University Policies'
        ordering = ['-published_date']

    def __str__(self):
        return self.title


class StrategicPlan(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    year = models.IntegerField()
    duration_years = models.IntegerField(default=5, help_text='Duration of strategic plan in years')
    description = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    strategic_goals = models.TextField(blank=True, help_text='Key objectives and goals')
    document = models.FileField(upload_to='policies/strategic_plans/', blank=True, help_text='PDF or Word document')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Strategic Plan'
        verbose_name_plural = 'Strategic Plans'
        ordering = ['-year']
        unique_together = ('year', 'slug')

    def __str__(self):
        return f"{self.title} ({self.year}-{self.year + self.duration_years - 1})"
