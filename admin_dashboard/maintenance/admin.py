from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Q
from .models import (
    MaintenanceTeam, Technician, MaintenanceRequest, MaintenanceWorkOrder,
    MaintenanceCompletion, MaintenanceSignature, MaintenanceSchedule,
    MaintenanceMetrics, MaintenanceHistory
)


@admin.register(MaintenanceTeam)
class MaintenanceTeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'head_technician', 'is_active', 'phone', 'email']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'email', 'phone']
    readonly_fields = ['created_at']


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'specialization', 'license_status', 'is_active', 'phone']
    list_filter = ['team', 'specialization', 'is_active', 'license_expiry']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'license_number', 'phone']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'team')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'license_number', 'license_expiry', 'phone')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def license_status(self, obj):
        if not obj.license_expiry:
            return format_html('<span style="color: #999;">N/A</span>')
        from datetime import date
        if obj.license_expiry < date.today():
            return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">EXPIRED</span>')
        return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">VALID</span>')
    license_status.short_description = 'License Status'


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'title', 'priority_badge', 'status_badge', 'requester', 'assigned_to', 'requested_date']
    list_filter = ['status', 'priority', 'requested_date', 'assigned_to__team']
    search_fields = ['request_id', 'title', 'description', 'requester__first_name', 'requester__last_name']
    readonly_fields = ['request_id', 'created_at', 'updated_at', 'requested_date']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('request_id', 'requester', 'title', 'description')
        }),
        ('Asset & Location', {
            'fields': ('asset', 'location_description')
        }),
        ('Priority & Status', {
            'fields': ('priority', 'status', 'target_completion_date')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'assigned_date')
        }),
        ('Additional Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('requested_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'requested_date'
    ordering = ['-requested_date']
    actions = ['mark_submitted', 'mark_acknowledged', 'mark_scheduled', 'mark_completed', 'mark_cancelled']

    def priority_badge(self, obj):
        colors = {
            'urgent': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#28a745',
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            'white' if obj.priority in ['urgent', 'high'] else 'black',
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'

    def status_badge(self, obj):
        colors = {
            'draft': '#6c757d',
            'submitted': '#007bff',
            'acknowledged': '#17a2b8',
            'scheduled': '#28a745',
            'in_progress': '#ffc107',
            'completed': '#20c997',
            'on_hold': '#e83e8c',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def mark_submitted(self, request, queryset):
        queryset.update(status='submitted')
    mark_submitted.short_description = 'Mark as Submitted'

    def mark_acknowledged(self, request, queryset):
        queryset.update(status='acknowledged')
    mark_acknowledged.short_description = 'Mark as Acknowledged'

    def mark_scheduled(self, request, queryset):
        queryset.update(status='scheduled')
    mark_scheduled.short_description = 'Mark as Scheduled'

    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = 'Mark as Completed'

    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_cancelled.short_description = 'Mark as Cancelled'


@admin.register(MaintenanceWorkOrder)
class MaintenanceWorkOrderAdmin(admin.ModelAdmin):
    list_display = [
        'work_order_id', 'maintenance_request', 'technician', 'status_badge',
        'scheduled_date', 'estimated_cost', 'actual_cost'
    ]
    list_filter = ['status', 'scheduled_date', 'technician__specialization']
    search_fields = ['work_order_id', 'maintenance_request__title', 'technician__user__first_name']
    readonly_fields = ['work_order_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Work Order Information', {
            'fields': ('work_order_id', 'maintenance_request', 'status')
        }),
        ('Assignment', {
            'fields': ('technician', 'supervisor')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'scheduled_start_time', 'scheduled_end_time', 'actual_start_time', 'actual_end_time')
        }),
        ('Work Details', {
            'fields': ('work_description', 'materials_required')
        }),
        ('Costs', {
            'fields': ('estimated_cost', 'actual_cost', 'currency')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'scheduled_date'
    ordering = ['-scheduled_date']

    def status_badge(self, obj):
        colors = {
            'pending': '#6c757d',
            'scheduled': '#007bff',
            'in_progress': '#ffc107',
            'completed': '#28a745',
            'on_hold': '#e83e8c',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(MaintenanceCompletion)
class MaintenanceCompletionAdmin(admin.ModelAdmin):
    list_display = ['work_order', 'completion_date', 'hours_worked', 'total_cost', 'asset_condition_after', 'follow_up_needed']
    list_filter = ['completion_date', 'asset_condition_after', 'follow_up_needed']
    search_fields = ['work_order__work_order_id', 'work_performed', 'parts_replaced']
    readonly_fields = ['completion_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Work Order', {
            'fields': ('work_order', 'completed_by', 'completion_date')
        }),
        ('Work Performed', {
            'fields': ('work_performed', 'materials_used', 'parts_replaced')
        }),
        ('Time & Cost', {
            'fields': ('hours_worked', 'labor_cost', 'parts_cost', 'total_cost', 'currency')
        }),
        ('Asset Condition', {
            'fields': ('asset_condition_after',)
        }),
        ('Follow-up', {
            'fields': ('follow_up_needed', 'follow_up_notes')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'completion_date'
    ordering = ['-completion_date']


@admin.register(MaintenanceSignature)
class MaintenanceSignatureAdmin(admin.ModelAdmin):
    list_display = ['work_order', 'signature_type_display', 'signer', 'is_valid', 'signature_timestamp']
    list_filter = ['signature_type', 'is_valid', 'signature_timestamp']
    search_fields = ['work_order__work_order_id', 'signer__first_name', 'signer__last_name']
    readonly_fields = ['signature_timestamp', 'created_at', 'signature_preview']
    
    fieldsets = (
        ('Signature Information', {
            'fields': ('work_order', 'signature_type', 'signer', 'is_valid')
        }),
        ('Signature Data', {
            'fields': ('signature_preview', 'ip_address', 'device_info')
        }),
        ('Comments', {
            'fields': ('comments',)
        }),
        ('Timestamps', {
            'fields': ('signature_timestamp', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'signature_timestamp'
    ordering = ['-signature_timestamp']

    def signature_type_display(self, obj):
        return obj.get_signature_type_display()
    signature_type_display.short_description = 'Type'

    def signature_preview(self, obj):
        if obj.signature_data:
            return format_html(
                '<img src="data:image/png;base64,{}" style="max-width: 300px; max-height: 150px; border: 1px solid #ddd; padding: 5px;" />',
                obj.signature_data
            )
        return "No signature data"
    signature_preview.short_description = 'Signature Preview'


@admin.register(MaintenanceSchedule)
class MaintenanceScheduleAdmin(admin.ModelAdmin):
    list_display = ['asset', 'title', 'frequency', 'last_performed', 'next_due_date', 'status_badge', 'estimated_duration_hours']
    list_filter = ['frequency', 'is_active', 'assigned_team', 'next_due_date']
    search_fields = ['asset__asset_tag', 'asset__name', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('asset', 'title', 'description')
        }),
        ('Frequency', {
            'fields': ('frequency', 'last_performed', 'next_due_date')
        }),
        ('Assignment & Estimates', {
            'fields': ('assigned_team', 'estimated_duration_hours', 'estimated_cost')
        }),
        ('Status & Notes', {
            'fields': ('is_active', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'next_due_date'
    ordering = ['next_due_date']

    def status_badge(self, obj):
        from datetime import date
        if not obj.is_active:
            return format_html('<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px;">INACTIVE</span>')
        if obj.next_due_date <= date.today():
            return format_html('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">OVERDUE</span>')
        return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">SCHEDULED</span>')
    status_badge.short_description = 'Status'


@admin.register(MaintenanceMetrics)
class MaintenanceMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'month', 'total_requests', 'completed_requests', 'total_maintenance_cost',
        'total_labor_hours', 'asset_availability_percent'
    ]
    list_filter = ['month']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Period', {
            'fields': ('month',)
        }),
        ('Request Metrics', {
            'fields': ('total_requests', 'completed_requests', 'average_completion_time_days', 'emergency_requests')
        }),
        ('Schedule Metrics', {
            'fields': ('scheduled_maintenance_completed',)
        }),
        ('Financial Metrics', {
            'fields': ('total_maintenance_cost', 'total_labor_hours')
        }),
        ('Performance Metrics', {
            'fields': ('downtime_hours', 'asset_availability_percent', 'repeat_maintenance_issues')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'month'
    ordering = ['-month']


@admin.register(MaintenanceHistory)
class MaintenanceHistoryAdmin(admin.ModelAdmin):
    list_display = ['asset', 'maintenance_date', 'technician', 'work_description', 'cost', 'duration_hours']
    list_filter = ['maintenance_date', 'asset__category', 'technician']
    search_fields = ['asset__asset_tag', 'asset__name', 'work_description', 'technician__user__first_name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Asset & Work Order', {
            'fields': ('asset', 'work_order')
        }),
        ('Maintenance Details', {
            'fields': ('maintenance_date', 'work_description', 'spare_parts_used')
        }),
        ('Personnel', {
            'fields': ('technician', 'supervisor')
        }),
        ('Time & Cost', {
            'fields': ('duration_hours', 'cost')
        }),
        ('Asset Condition', {
            'fields': ('asset_condition_before', 'asset_condition_after')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'maintenance_date'
    ordering = ['-maintenance_date']
