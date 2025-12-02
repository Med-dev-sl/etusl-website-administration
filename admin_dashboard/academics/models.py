from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    """University department (e.g., Engineering, Arts, Sciences)"""
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    office_location = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='departments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Program(models.Model):
    """Academic programs/degrees (e.g., BSc Computer Science)"""
    LEVEL_CHOICES = [
        ('diploma', 'Diploma'),
        ('bachelors', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('phd', 'PhD'),
    ]
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField(blank=True)
    duration_months = models.IntegerField(help_text="Duration in months")
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    entry_requirements = models.TextField(blank=True)
    career_prospects = models.TextField(blank=True)
    program_coordinator = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['department', 'name']

    def __str__(self):
        return f"{self.name} ({self.department.name})"


class Course(models.Model):
    """Courses offered within a program"""
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=10, unique=True)  # e.g., "CS101"
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    credits = models.IntegerField(default=3, help_text="Credit hours")
    semester = models.IntegerField(help_text="Semester this course is offered")
    instructor = models.CharField(max_length=255, blank=True)
    is_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['program', 'semester', 'code']
        unique_together = ('program', 'code')

    def __str__(self):
        return f"{self.code} - {self.title}"


class Faculty(models.Model):
    """Faculty/staff members linked to departments"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='faculty')
    title = models.CharField(max_length=255, blank=True)  # e.g., "Professor", "Lecturer"
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    office_room = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='faculty/', null=True, blank=True)
    publications = models.TextField(blank=True, help_text="Research publications or achievements")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['department', 'full_name']

    def __str__(self):
        return f"{self.full_name} ({self.department.name if self.department else 'No Dept'})"
