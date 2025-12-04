from django.contrib import admin
from .models import Department, VisitRequest


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'requester', 'department', 'status', 'created_at', 'responded_at')
    list_filter = ('status', 'department', 'created_at')
    search_fields = ('requester__username', 'requester__email', 'reason', 'head_note')
    readonly_fields = ('created_at', 'responded_at')
    fields = (
        'requester', 'department', 'reason', 'created_by_secretary',
        'status', 'head_note', 'responded_by', 'responded_at', 'created_at'
    )
