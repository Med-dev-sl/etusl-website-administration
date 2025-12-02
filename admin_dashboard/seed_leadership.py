#!/usr/bin/env python
"""
Seed leadership data with linked user accounts
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')
django.setup()

from django.contrib.auth.models import User
from staff.models import Leadership

# Create a leader user (if doesn't exist)
leader_user, _ = User.objects.get_or_create(
    username='rector',
    defaults={
        'email': 'rector@etusl.edu',
        'first_name': 'Dr.',
        'last_name': 'Mensah',
    }
)
print(f"✓ User created/exists: {leader_user.username} ({leader_user.email})")

# Create Leadership entry linked to the user
leadership, created = Leadership.objects.get_or_create(
    user=leader_user,
    defaults={
        'full_name': 'Dr. Kwesi Mensah',
        'position': 'Vice Chancellor (Rector)',
        'email': 'rector@etusl.edu',
        'phone': '+233-XXX-XXX-XXXX',
        'biography': '''Dr. Kwesi Mensah is the Vice Chancellor of ETUSL with over 20 years of experience in higher education leadership. 
He holds a PhD in Educational Administration from a leading African institution and has been instrumental in the university's expansion and modernization initiatives.

Dr. Mensah is passionate about fostering academic excellence, research innovation, and student welfare. He has published extensively in peer-reviewed journals 
and is a sought-after speaker at international educational conferences.''',
        'is_active': True,
    }
)

if created:
    print(f"✓ Leadership record created: {leadership.full_name}")
else:
    print(f"✓ Leadership record already exists: {leadership.full_name}")

print("\n✅ Leadership seeding completed!")
print(f"   User: {leader_user.username}")
print(f"   Position: {leadership.position}")
print(f"   Email: {leadership.email}")
print(f"\nLeader can now log in with username '{leader_user.username}' and edit their profile at /staff/leadership/edit/")
