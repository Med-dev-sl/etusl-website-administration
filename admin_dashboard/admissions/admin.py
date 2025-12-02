from django.contrib import admin
from .models import AdmissionCycle, Requirement, Applicant, UploadedDocument


@admin.register(AdmissionCycle)
class AdmissionCycleAdmin(admin.ModelAdmin):
    list_display = ('year', 'start_date', 'end_date', 'application_deadline', 'is_active')
    list_filter = ('is_active', 'year')
    date_hierarchy = 'start_date'


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'document_type', 'is_mandatory')
    list_filter = ('program', 'is_mandatory')
    search_fields = ('title', 'program__name')


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'program', 'status', 'applied_at')
    list_filter = ('status', 'program', 'admission_cycle', 'applied_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    date_hierarchy = 'applied_at'
    readonly_fields = ('applied_at', 'updated_at')


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'requirement', 'uploaded_at')
    list_filter = ('requirement', 'uploaded_at')
    search_fields = ('applicant__first_name', 'applicant__last_name')
