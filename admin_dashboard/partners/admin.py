from django.contrib import admin
from .models import Partner, Affiliate


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'contact_email', 'is_active', 'start_date')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'website', 'contact_email')
    list_filter = ('is_active',)


@admin.register(Affiliate)
class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner', 'contact_email', 'added_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'partner__name', 'contact_email')
    list_filter = ('partner',)
