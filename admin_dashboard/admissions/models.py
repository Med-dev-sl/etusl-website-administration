from django.db import models


class AdmissionCycle(models.Model):
    """Admission cycles for the university"""
    year = models.IntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    application_deadline = models.DateField()
    result_announcement_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"Admission Cycle {self.year}"


class Requirement(models.Model):
    """Admission requirements for programs"""
    from academics.models import Program
    
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='admission_requirements')
    title = models.CharField(max_length=255)
    description = models.TextField()
    document_type = models.CharField(max_length=100, blank=True)  # e.g., "Birth Certificate", "Passport"
    is_mandatory = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['program', 'is_mandatory', 'title']

    def __str__(self):
        return f"{self.program.name} - {self.title}"


class Applicant(models.Model):
    """Student applicants"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('enrolled', 'Enrolled'),
    ]
    
    admission_cycle = models.ForeignKey(AdmissionCycle, on_delete=models.SET_NULL, null=True, related_name='applicants')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100, blank=True)
    program = models.ForeignKey('academics.Program', on_delete=models.SET_NULL, null=True, related_name='applicants')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, help_text="GPA or equivalent score")
    documents_uploaded = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UploadedDocument(models.Model):
    """Documents uploaded by applicants"""
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='documents')
    requirement = models.ForeignKey(Requirement, on_delete=models.SET_NULL, null=True, blank=True)
    document_file = models.FileField(upload_to='applicant_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.first_name} - {self.requirement.title if self.requirement else 'Other'}"

