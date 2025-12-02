from django.contrib import admin
from .models import StaffMember, Leadership


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'title', 'email')


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'email', 'is_active')
    search_fields = ('full_name', 'position', 'email')
    list_filter = ('is_active',)
