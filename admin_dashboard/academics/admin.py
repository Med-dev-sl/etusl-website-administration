from django.contrib import admin
from .models import Department, Program, Course, Faculty


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department', 'email', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name', 'head_of_department')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'level', 'duration_months', 'is_active')
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('level', 'department', 'is_active')
    search_fields = ('name', 'department__name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'program', 'semester', 'credits', 'is_required')
    list_filter = ('program', 'semester', 'is_required')
    search_fields = ('code', 'title', 'program__name')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'title', 'email', 'created_at')
    list_filter = ('department', 'title')
    search_fields = ('full_name', 'email', 'department__name')
