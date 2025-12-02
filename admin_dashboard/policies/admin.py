from django.contrib import admin
from .models import UniversityPolicy, StrategicPlan


@admin.register(UniversityPolicy)
class UniversityPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'published_date')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('category', 'is_active', 'published_date')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category')
        }),
        ('Content', {
            'fields': ('description', 'content')
        }),
        ('Document', {
            'fields': ('document',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ('published_date', 'last_updated', 'created_at')


@admin.register(StrategicPlan)
class StrategicPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'duration_years', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'vision', 'mission', 'strategic_goals')
    list_filter = ('is_active', 'year')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'year', 'duration_years')
        }),
        ('Strategic Content', {
            'fields': ('description', 'vision', 'mission', 'strategic_goals')
        }),
        ('Document', {
            'fields': ('document',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
