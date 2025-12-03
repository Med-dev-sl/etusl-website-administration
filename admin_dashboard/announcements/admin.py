from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    AnnouncementCategory, Announcement, AnnouncementAcknowledgment,
    AnnouncementComment, AnnouncementAttachment, AnnouncementDistribution,
    AnnouncementTemplate, AnnouncementAnalytics
)


@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_badge', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def color_badge(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            obj.color,
            obj.name
        )
    color_badge.short_description = 'Category'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status_badge', 'priority_badge', 'is_featured_icon',
        'view_count', 'published_at', 'created_by'
    ]
    list_filter = ['status', 'priority', 'category', 'is_featured', 'is_sticky', 'published_at']
    search_fields = ['title', 'content', 'summary', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'view_count', 'slug']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'summary', 'content', 'category')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Priority & Status', {
            'fields': ('priority', 'status')
        }),
        ('Publishing Schedule', {
            'fields': ('published_at', 'expiry_at')
        }),
        ('Visibility & Engagement', {
            'fields': ('is_featured', 'is_sticky', 'target_audience', 'allow_comments', 'require_acknowledgment')
        }),
        ('Metadata', {
            'fields': ('tags', 'keywords', 'view_count')
        }),
        ('Author & Timestamps', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    date_hierarchy = 'published_at'
    ordering = ['-published_at']
    actions = ['publish_announcements', 'expire_announcements', 'archive_announcements', 'mark_featured', 'unmark_featured']

    def status_badge(self, obj):
        colors = {
            'draft': '#6c757d',
            'scheduled': '#007bff',
            'published': '#28a745',
            'expired': '#ffc107',
            'archived': '#868e96',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def priority_badge(self, obj):
        colors = {
            'low': '#28a745',
            'normal': '#17a2b8',
            'high': '#fd7e14',
            'urgent': '#dc3545',
        }
        color = colors.get(obj.priority, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'

    def is_featured_icon(self, obj):
        if obj.is_featured:
            return format_html('<span style="color: #ffc107; font-size: 16px;">★</span>')
        return format_html('<span style="color: #ccc; font-size: 16px;">☆</span>')
    is_featured_icon.short_description = 'Featured'

    def publish_announcements(self, request, queryset):
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} announcements published.')
    publish_announcements.short_description = 'Publish selected announcements'

    def expire_announcements(self, request, queryset):
        updated = queryset.update(status='expired')
        self.message_user(request, f'{updated} announcements marked as expired.')
    expire_announcements.short_description = 'Mark selected as expired'

    def archive_announcements(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} announcements archived.')
    archive_announcements.short_description = 'Archive selected announcements'

    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} announcements marked as featured.')
    mark_featured.short_description = 'Mark as featured'

    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} announcements unmarked as featured.')
    unmark_featured.short_description = 'Unmark as featured'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AnnouncementAcknowledgment)
class AnnouncementAcknowledgmentAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'user', 'acknowledged_at']
    list_filter = ['acknowledged_at', 'announcement__category']
    search_fields = ['announcement__title', 'user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['acknowledged_at']
    ordering = ['-acknowledged_at']
    
    fieldsets = (
        ('Acknowledgment Information', {
            'fields': ('announcement', 'user', 'acknowledged_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )

    date_hierarchy = 'acknowledged_at'


@admin.register(AnnouncementComment)
class AnnouncementCommentAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'commenter', 'approval_badge', 'created_at']
    list_filter = ['is_approved', 'created_at', 'announcement__category']
    search_fields = ['announcement__title', 'commenter__first_name', 'commenter__last_name', 'content']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_comments', 'disapprove_comments']
    
    ordering = ['-created_at']

    def approval_badge(self, obj):
        if obj.is_approved:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Approved</span>')
        return format_html('<span style="background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 3px;">Pending</span>')
    approval_badge.short_description = 'Status'

    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments approved.')
    approve_comments.short_description = 'Approve selected comments'

    def disapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'


@admin.register(AnnouncementAttachment)
class AnnouncementAttachmentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'announcement', 'file_type', 'download_count', 'uploaded_at', 'uploaded_by']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['filename', 'announcement__title']
    readonly_fields = ['uploaded_at', 'download_count', 'file_type']
    
    fieldsets = (
        ('Attachment Information', {
            'fields': ('announcement', 'file', 'filename', 'file_type')
        }),
        ('Upload Details', {
            'fields': ('uploaded_by', 'uploaded_at', 'download_count')
        }),
    )

    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']


@admin.register(AnnouncementDistribution)
class AnnouncementDistributionAdmin(admin.ModelAdmin):
    list_display = [
        'announcement', 'distribution_method', 'status_badge', 'recipient_group',
        'success_count', 'failure_count', 'sent_at'
    ]
    list_filter = ['status', 'distribution_method', 'created_at']
    search_fields = ['announcement__title', 'recipient_group']
    readonly_fields = ['sent_at', 'created_at']
    
    fieldsets = (
        ('Distribution Information', {
            'fields': ('announcement', 'distribution_method', 'recipient_group')
        }),
        ('Scheduling', {
            'fields': ('status', 'scheduled_for', 'sent_at')
        }),
        ('Results', {
            'fields': ('recipient_count', 'success_count', 'failure_count', 'failure_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'pending': '#007bff',
            'sent': '#28a745',
            'failed': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(AnnouncementTemplate)
class AnnouncementTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'description', 'content_template']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'description', 'category', 'is_active')
        }),
        ('Content', {
            'fields': ('content_template',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AnnouncementAnalytics)
class AnnouncementAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'announcement', 'total_views', 'unique_viewers', 'total_comments',
        'total_acknowledgments', 'attachment_downloads', 'last_updated'
    ]
    list_filter = ['last_updated']
    search_fields = ['announcement__title']
    readonly_fields = [
        'total_views', 'unique_viewers', 'total_comments', 'approved_comments',
        'total_acknowledgments', 'acknowledged_count', 'attachment_downloads',
        'average_time_spent_seconds', 'last_updated'
    ]

    fieldsets = (
        ('Announcement', {
            'fields': ('announcement',)
        }),
        ('View Analytics', {
            'fields': ('total_views', 'unique_viewers', 'average_time_spent_seconds')
        }),
        ('Engagement', {
            'fields': ('total_comments', 'approved_comments', 'attachment_downloads')
        }),
        ('Acknowledgments', {
            'fields': ('total_acknowledgments', 'acknowledged_count')
        }),
        ('Timestamps', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
