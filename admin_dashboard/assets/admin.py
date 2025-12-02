from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AssetCategory, AssetLocation, Asset, AssetMovement,
    InventoryItem, InventoryTransaction, MaintenanceRecord
)


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(AssetLocation)
class AssetLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'is_active', 'created_at']
    list_filter = ['is_active', 'department', 'created_at']
    search_fields = ['name', 'department', 'description']
    ordering = ['department', 'name']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = [
        'asset_tag', 'name', 'category', 'status_badge',
        'condition', 'current_location', 'assigned_to', 'purchase_price'
    ]
    list_filter = ['status', 'condition', 'category', 'current_location', 'acquisition_date']
    search_fields = ['asset_tag', 'name', 'serial_number', 'description']
    readonly_fields = ['created_at', 'updated_at', 'depreciated_value', 'years_in_service', 'created_by']
    
    fieldsets = (
        ('Asset Information', {
            'fields': ('asset_tag', 'name', 'description', 'category', 'serial_number')
        }),
        ('Financial Details', {
            'fields': ('purchase_price', 'current_value', 'currency', 'depreciation_rate', 'depreciated_value')
        }),
        ('Lifecycle', {
            'fields': ('acquisition_date', 'warranty_expiry', 'years_in_service', 'status', 'condition')
        }),
        ('Current Assignment', {
            'fields': ('current_location', 'assigned_to')
        }),
        ('Maintenance', {
            'fields': ('last_maintenance_date', 'maintenance_notes')
        }),
        ('Tracking', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'acquisition_date'
    ordering = ['-created_at']

    def status_badge(self, obj):
        colors = {
            'active': '#28a745',
            'inactive': '#6c757d',
            'damaged': '#ffc107',
            'disposed': '#dc3545',
            'lost': '#e83e8c',
            'maintenance': '#007bff',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AssetMovement)
class AssetMovementAdmin(admin.ModelAdmin):
    list_display = [
        'asset', 'movement_type', 'from_location', 'to_location',
        'quantity', 'movement_date', 'recorded_by'
    ]
    list_filter = ['movement_type', 'movement_date', 'asset__category']
    search_fields = ['asset__asset_tag', 'asset__name', 'reference_document']
    readonly_fields = ['movement_date', 'recorded_by']
    
    fieldsets = (
        ('Movement Details', {
            'fields': ('asset', 'movement_type', 'quantity')
        }),
        ('From', {
            'fields': ('from_location', 'from_user')
        }),
        ('To', {
            'fields': ('to_location', 'to_user')
        }),
        ('Additional Information', {
            'fields': ('reference_document', 'notes', 'movement_date', 'recorded_by')
        }),
    )
    
    date_hierarchy = 'movement_date'
    ordering = ['-movement_date']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = [
        'item_code', 'name', 'quantity_on_hand', 'reorder_level',
        'restock_status', 'unit_cost', 'total_value', 'storage_location'
    ]
    list_filter = ['category', 'is_active', 'storage_location', 'last_restocked']
    search_fields = ['item_code', 'name', 'supplier', 'description']
    readonly_fields = ['created_at', 'updated_at', 'total_value']
    
    fieldsets = (
        ('Item Information', {
            'fields': ('item_code', 'name', 'description', 'category')
        }),
        ('Inventory Levels', {
            'fields': ('quantity_on_hand', 'reorder_level', 'reorder_quantity', 'unit')
        }),
        ('Financial', {
            'fields': ('unit_cost', 'currency', 'total_value')
        }),
        ('Location & Supplier', {
            'fields': ('storage_location', 'supplier', 'is_active')
        }),
        ('Tracking', {
            'fields': ('created_at', 'updated_at', 'last_restocked'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['category', 'name']

    def restock_status(self, obj):
        if obj.needs_reorder():
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">REORDER NEEDED</span>'
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">OK</span>'
        )
    restock_status.short_description = 'Restock Status'


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'item', 'transaction_type', 'quantity', 'issued_to',
        'issued_by', 'transaction_date'
    ]
    list_filter = ['transaction_type', 'transaction_date', 'item__category']
    search_fields = ['item__item_code', 'item__name', 'reference_document', 'issued_to__username']
    readonly_fields = ['transaction_date', 'issued_by']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('item', 'transaction_type', 'quantity')
        }),
        ('Parties', {
            'fields': ('issued_to', 'issued_by')
        }),
        ('Reference', {
            'fields': ('reference_document', 'notes', 'transaction_date')
        }),
    )
    
    date_hierarchy = 'transaction_date'
    ordering = ['-transaction_date']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.issued_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = [
        'asset', 'title', 'scheduled_date', 'status_badge',
        'assigned_to', 'cost', 'completion_date'
    ]
    list_filter = ['status', 'scheduled_date', 'asset__category']
    search_fields = ['asset__asset_tag', 'asset__name', 'title', 'description']
    readonly_fields = ['created_at', 'created_by']
    
    fieldsets = (
        ('Maintenance Details', {
            'fields': ('asset', 'title', 'description')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'completion_date', 'status')
        }),
        ('Cost & Assignment', {
            'fields': ('cost', 'currency', 'assigned_to')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Tracking', {
            'fields': ('created_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'scheduled_date'
    ordering = ['-scheduled_date']

    def status_badge(self, obj):
        colors = {
            'scheduled': '#007bff',
            'in_progress': '#ffc107',
            'completed': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
