#!/usr/bin/env python
"""
Seed Announcements data
"""
import os
import django
from datetime import date, datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')
django.setup()

from django.contrib.auth.models import User
from announcements.models import (
    AnnouncementCategory, Announcement, AnnouncementTemplate,
    AnnouncementDistribution
)

admin_user = User.objects.filter(username='ETUSLWEB001').first() or User.objects.filter(is_superuser=True).first()

print("=" * 70)
print("SEEDING ANNOUNCEMENTS DATA")
print("=" * 70)

# ===== Announcement Categories =====
categories_data = [
    {
        'name': 'Academic',
        'slug': 'academic',
        'description': 'Academic news, exam schedules, course updates',
        'color': '#007bff',
        'icon': 'fa-graduation-cap'
    },
    {
        'name': 'Administrative',
        'slug': 'administrative',
        'description': 'University policies, administrative updates',
        'color': '#6c757d',
        'icon': 'fa-building'
    },
    {
        'name': 'Events',
        'slug': 'events',
        'description': 'Upcoming events, conferences, workshops',
        'color': '#28a745',
        'icon': 'fa-calendar'
    },
    {
        'name': 'Maintenance',
        'slug': 'maintenance',
        'description': 'Facility maintenance, building closures',
        'color': '#ffc107',
        'icon': 'fa-wrench'
    },
    {
        'name': 'Emergency',
        'slug': 'emergency',
        'description': 'Urgent safety announcements',
        'color': '#dc3545',
        'icon': 'fa-exclamation-triangle'
    },
    {
        'name': 'General',
        'slug': 'general',
        'description': 'General university announcements',
        'color': '#17a2b8',
        'icon': 'fa-bullhorn'
    },
]

categories = {}
for cat_data in categories_data:
    cat, created = AnnouncementCategory.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
            'color': cat_data['color'],
            'icon': cat_data['icon'],
            'is_active': True,
        }
    )
    categories[cat_data['slug']] = cat
    if created:
        print(f"✓ Announcement Category created: {cat.name}")

# ===== Announcements =====
announcements_data = [
    {
        'title': 'Final Examination Schedule Released',
        'slug': 'final-exam-schedule-2025',
        'summary': 'Final examination schedule for the 2024/2025 academic year is now available',
        'content': '''The final examination schedule for the 2024/2025 academic year has been released and is now available on the student portal.

**Key Dates:**
- Examination Period: December 15, 2025 - January 20, 2026
- Registration Deadline: December 10, 2025
- Appeals Deadline: January 25, 2026

**Important Notes:**
- Students must register for their exams by the deadline
- Bring valid ID to all examination halls
- Examination halls open 15 minutes before scheduled time
- Late arrivals (after 15 minutes) will not be admitted

For detailed schedule, visit: student-portal.etusl.edu/exams''',
        'category': 'academic',
        'priority': 'high',
        'status': 'published',
        'is_featured': True,
        'is_sticky': True,
        'target_audience': 'students',
        'published_offset': -5,
    },
    {
        'title': 'Campus WiFi Maintenance on December 5th',
        'slug': 'wifi-maintenance-dec-5',
        'summary': 'WiFi services will be temporarily unavailable for maintenance',
        'content': '''All wireless network services will be unavailable for maintenance on December 5th, 2025.

**Affected Period:** 02:00 AM - 06:00 AM GMT

**Impact:**
- WiFi services will be down across all campus locations
- Wired network connections will remain available
- Online classes should be rescheduled if possible

We apologize for any inconvenience caused. If you have any questions, contact IT Support.''',
        'category': 'maintenance',
        'priority': 'normal',
        'status': 'published',
        'is_featured': False,
        'is_sticky': False,
        'target_audience': 'all',
        'published_offset': -2,
    },
    {
        'title': 'Annual Research Conference - Call for Papers',
        'slug': 'research-conference-call-for-papers',
        'summary': 'Submit your research papers for the Annual Research Conference 2026',
        'content': '''The Department of Research & Innovation invites submissions for the Annual Research Conference 2026.

**Conference Details:**
- Date: March 15-17, 2026
- Location: University Conference Center
- Theme: "Innovation in Higher Education"

**Submission Guidelines:**
- Abstract: 250-350 words
- Full Paper: 5000-7000 words
- Deadline: January 31, 2026
- Contact: research@etusl.edu

All faculty, students, and visiting scholars are welcome to submit.''',
        'category': 'events',
        'priority': 'normal',
        'status': 'published',
        'is_featured': True,
        'is_sticky': False,
        'target_audience': 'all',
        'published_offset': -1,
    },
    {
        'title': 'New Academic Calendar for 2025/2026',
        'slug': 'academic-calendar-2025-2026',
        'summary': 'The official academic calendar for 2025/2026 has been released',
        'content': '''The new academic calendar for 2025/2026 has been officially approved and released.

**Key Dates:**
- Semester 1 Start: September 15, 2025
- Mid-Semester Break: October 20-24, 2025
- Semester 1 End: December 10, 2025
- Semester 2 Start: January 12, 2026
- Semester 2 End: May 15, 2026

All departments must align with this calendar.''',
        'category': 'academic',
        'priority': 'high',
        'status': 'published',
        'is_featured': True,
        'is_sticky': False,
        'target_audience': 'all',
        'published_offset': -10,
    },
    {
        'title': 'Library Extended Hours - Exam Period',
        'slug': 'library-extended-hours-exam',
        'summary': 'Library will have extended operating hours during examination period',
        'content': '''To support students during examination period, the Main Library will extend its operating hours.

**Extended Hours (December 15 - January 20):**
- Monday - Friday: 07:00 AM - 11:00 PM
- Saturday: 09:00 AM - 09:00 PM
- Sunday: 10:00 AM - 08:00 PM

Study spaces and computer facilities will be available during all extended hours.''',
        'category': 'academic',
        'priority': 'normal',
        'status': 'published',
        'is_featured': False,
        'is_sticky': False,
        'target_audience': 'students',
        'published_offset': -3,
    },
    {
        'title': 'Important: Update Your Emergency Contact Information',
        'slug': 'emergency-contact-update',
        'summary': 'All staff and students must update emergency contact information',
        'content': '''This is an important reminder to update your emergency contact information in the student/staff portal.

**How to Update:**
1. Log in to your portal account
2. Go to Personal Information
3. Update Emergency Contacts
4. Click Save

This information is crucial for university safety and emergency procedures. All updates must be completed by December 31, 2025.''',
        'category': 'administrative',
        'priority': 'high',
        'status': 'published',
        'is_featured': True,
        'is_sticky': True,
        'target_audience': 'all',
        'published_offset': -1,
        'require_acknowledgment': True,
    },
]

announcements = []
for ann_data in announcements_data:
    pub_date = timezone.now() - timedelta(days=ann_data['published_offset'])
    
    ann, created = Announcement.objects.get_or_create(
        slug=ann_data['slug'],
        defaults={
            'title': ann_data['title'],
            'summary': ann_data['summary'],
            'content': ann_data['content'],
            'category': categories[ann_data['category']],
            'priority': ann_data['priority'],
            'status': ann_data['status'],
            'created_by': admin_user,
            'published_at': pub_date,
            'is_featured': ann_data['is_featured'],
            'is_sticky': ann_data['is_sticky'],
            'target_audience': ann_data['target_audience'],
            'require_acknowledgment': ann_data.get('require_acknowledgment', False),
            'tags': 'important,announcement',
        }
    )
    
    if created:
        # Create analytics record
        from announcements.models import AnnouncementAnalytics
        AnnouncementAnalytics.objects.create(announcement=ann)
        print(f"✓ Announcement created: {ann.title}")
    announcements.append(ann)

# ===== Announcement Templates =====
templates_data = [
    {
        'name': 'Course Update Template',
        'description': 'Template for course-related updates',
        'category': 'academic',
        'content': '''Subject: {{course_name}} - Important Update

Dear Students,

We have an important update regarding {{course_name}}.

**Update Details:**
{{update_details}}

**Action Required:**
{{action_required}}

Please contact your instructor if you have questions.

Best regards,
Academic Department'''
    },
    {
        'name': 'Maintenance Notice Template',
        'description': 'Template for maintenance notifications',
        'category': 'maintenance',
        'content': '''MAINTENANCE NOTICE

The following facility maintenance is scheduled:

**Location:** {{location}}
**Date/Time:** {{date_time}}
**Duration:** {{duration}}
**Impact:** {{impact}}

We apologize for any inconvenience.'''
    },
    {
        'name': 'Event Announcement Template',
        'description': 'Template for event announcements',
        'category': 'events',
        'content': '''{{event_name}} - Announcement

We are pleased to announce:

**Event:** {{event_name}}
**Date:** {{event_date}}
**Time:** {{event_time}}
**Location:** {{event_location}}
**Description:** {{event_description}}

**Registration:** {{registration_details}}

For more information, visit: {{event_link}}'''
    },
]

for tmpl_data in templates_data:
    tmpl, created = AnnouncementTemplate.objects.get_or_create(
        name=tmpl_data['name'],
        defaults={
            'description': tmpl_data['description'],
            'category': categories.get(tmpl_data['category']),
            'content_template': tmpl_data['content'],
            'created_by': admin_user,
            'is_active': True,
        }
    )
    
    if created:
        print(f"✓ Announcement Template created: {tmpl.name}")

# ===== Announcement Distributions =====
if announcements:
    for ann in announcements[:2]:
        dist, created = AnnouncementDistribution.objects.get_or_create(
            announcement=ann,
            distribution_method='dashboard',
            defaults={
                'recipient_group': 'All Users',
                'recipient_count': 500,
                'status': 'sent',
                'sent_at': timezone.now(),
                'success_count': 500,
                'failure_count': 0,
            }
        )
        
        if created:
            print(f"✓ Announcement Distribution created: {ann.title}")

print("\n" + "=" * 70)
print("✅ ANNOUNCEMENTS SEEDING COMPLETED!")
print("=" * 70)
print(f"• Announcement Categories: {AnnouncementCategory.objects.count()}")
print(f"• Announcements: {Announcement.objects.count()}")
print(f"• Templates: {AnnouncementTemplate.objects.count()}")
print(f"• Distributions: {AnnouncementDistribution.objects.count()}")
print("=" * 70)
