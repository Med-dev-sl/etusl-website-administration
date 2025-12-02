from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AnnouncementCategory(models.Model):
    """Categories for announcements"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code for display')
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Announcement Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Announcement(models.Model):
    """Main announcements model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('expired', 'Expired'),
        ('archived', 'Archived'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Basic Information
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    summary = models.CharField(max_length=500, blank=True, help_text='Brief summary for listings')
    
    # Category & Priority
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.PROTECT, related_name='announcements')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Featured Image
    featured_image = models.ImageField(
        upload_to='announcements_images/',
        null=True,
        blank=True,
        help_text='Featured image for announcement'
    )
    
    # Publishing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements_created')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    published_at = models.DateTimeField(null=True, blank=True, help_text='When announcement becomes visible')
    expiry_at = models.DateTimeField(null=True, blank=True, help_text='When announcement becomes expired')
    
    # Visibility & Targeting
    is_featured = models.BooleanField(default=False, help_text='Show in featured section')
    is_sticky = models.BooleanField(default=False, help_text='Pin to top of announcements')
    
    target_audience = models.CharField(
        max_length=100,
        choices=[
            ('all', 'All Users'),
            ('students', 'Students Only'),
            ('staff', 'Staff Only'),
            ('faculty', 'Faculty Only'),
            ('admin', 'Admin Only'),
            ('specific', 'Specific Groups'),
        ],
        default='all'
    )
    
    # Engagement
    view_count = models.IntegerField(default=0)
    allow_comments = models.BooleanField(default=True)
    require_acknowledgment = models.BooleanField(default=False, help_text='Users must acknowledge receipt')
    
    # Metadata
    tags = models.CharField(max_length=500, blank=True, help_text='Comma-separated tags')
    keywords = models.TextField(blank=True, help_text='SEO keywords')
    
    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['priority']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def is_published(self):
        """Check if announcement is currently published"""
        now = timezone.now()
        if self.status != 'published':
            return False
        if self.published_at and self.published_at > now:
            return False
        if self.expiry_at and self.expiry_at < now:
            return False
        return True


class AnnouncementAcknowledgment(models.Model):
    """Track user acknowledgments of announcements"""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='acknowledgments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    acknowledged_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Announcement Acknowledgment'
        verbose_name_plural = 'Announcement Acknowledgments'
        unique_together = ['announcement', 'user']
        ordering = ['-acknowledged_at']

    def __str__(self):
        return f"{self.announcement.title} - {self.user.get_full_name()}"


class AnnouncementComment(models.Model):
    """Comments on announcements"""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content = models.TextField()
    
    is_approved = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Announcement Comment'
        verbose_name_plural = 'Announcement Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.commenter.get_full_name()} on {self.announcement.title}"


class AnnouncementAttachment(models.Model):
    """Attachments for announcements"""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='attachments')
    
    file = models.FileField(upload_to='announcements_attachments/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, blank=True, help_text='e.g., PDF, DOC, XLS')
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcement_attachments_uploaded')
    
    download_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Announcement Attachment'
        verbose_name_plural = 'Announcement Attachments'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.filename} - {self.announcement.title}"

    def save(self, *args, **kwargs):
        if self.file:
            self.filename = self.file.name
            import os
            self.file_type = os.path.splitext(self.file.name)[1].lstrip('.')
        super().save(*args, **kwargs)


class AnnouncementDistribution(models.Model):
    """Track announcement distribution to specific groups"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]

    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='distributions')
    
    distribution_method = models.CharField(
        max_length=50,
        choices=[
            ('email', 'Email'),
            ('sms', 'SMS'),
            ('push', 'Push Notification'),
            ('dashboard', 'Dashboard Display'),
            ('all', 'All Channels'),
        ],
        default='dashboard'
    )
    
    recipient_group = models.CharField(max_length=100, help_text='Target group/department')
    recipient_count = models.IntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    success_count = models.IntegerField(default=0)
    failure_count = models.IntegerField(default=0)
    failure_reason = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Announcement Distribution'
        verbose_name_plural = 'Announcement Distributions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.announcement.title} - {self.get_distribution_method_display()}"


class AnnouncementTemplate(models.Model):
    """Reusable announcement templates"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    content_template = models.TextField(help_text='Use {{field}} for placeholders')
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcement_templates_created')
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Announcement Template'
        verbose_name_plural = 'Announcement Templates'
        ordering = ['name']

    def __str__(self):
        return self.name


class AnnouncementAnalytics(models.Model):
    """Analytics for announcements"""
    announcement = models.OneToOneField(Announcement, on_delete=models.CASCADE, related_name='analytics')
    
    total_views = models.IntegerField(default=0)
    unique_viewers = models.IntegerField(default=0)
    
    total_comments = models.IntegerField(default=0)
    approved_comments = models.IntegerField(default=0)
    
    total_acknowledgments = models.IntegerField(default=0)
    acknowledged_count = models.IntegerField(default=0)
    
    attachment_downloads = models.IntegerField(default=0)
    
    average_time_spent_seconds = models.IntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Announcement Analytics'
        verbose_name_plural = 'Announcement Analytics'

    def __str__(self):
        return f"Analytics - {self.announcement.title}"
