from django.contrib import admin
from .models import NewsPost


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'published_at')
    prepopulated_fields = {"slug": ("title",)}
