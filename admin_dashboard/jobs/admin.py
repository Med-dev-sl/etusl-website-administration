from django.contrib import admin
from .models import JobPosting, JobApplication


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'job_type', 'deadline', 'is_active', 'application_count')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'department', 'position')
    list_filter = ('job_type', 'is_active', 'posted_date', 'deadline')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'department', 'position', 'job_type')
        }),
        ('Job Description', {
            'fields': ('description', 'requirements')
        }),
        ('Compensation', {
            'fields': ('salary_min', 'salary_max', 'currency'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('deadline', 'posted_date')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ('posted_date', 'created_at', 'updated_at')

    def application_count(self, obj):
        count = obj.applications.count()
        return f"{count} application{'s' if count != 1 else ''}"
    application_count.short_description = 'Applications'


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job', 'email', 'status', 'applied_at')
    search_fields = ('first_name', 'last_name', 'email', 'job__title')
    list_filter = ('status', 'job', 'applied_at')
    readonly_fields = ('applied_at', 'updated_at', 'job')
    fieldsets = (
        ('Applicant Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Job & Application', {
            'fields': ('job', 'resume')
        }),
        ('Application Details', {
            'fields': ('cover_letter', 'status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Applicant'
