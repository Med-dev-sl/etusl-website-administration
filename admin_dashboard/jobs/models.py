from django.db import models
from django.utils import timezone


class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    department = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='full-time')
    description = models.TextField()
    requirements = models.TextField(blank=True)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='USD', help_text='Currency code (USD, GHS, EUR, etc.)')
    deadline = models.DateField()
    posted_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'
        ordering = ['-posted_date']

    def __str__(self):
        return self.title

    def is_open(self):
        return self.is_active and self.deadline >= timezone.now().date()


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='jobs/resumes/')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    notes = models.TextField(blank=True, help_text='Internal notes for recruitment team')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        ordering = ['-applied_at']
        unique_together = ('job', 'email')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job.title}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
