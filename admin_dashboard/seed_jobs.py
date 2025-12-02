#!/usr/bin/env python
"""
Seed Job Postings and sample applications
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')
django.setup()

from jobs.models import JobPosting, JobApplication

# Create sample job postings
jobs_data = [
    {
        'title': 'Senior Lecturer in Computer Science',
        'slug': 'senior-lecturer-computer-science',
        'department': 'Engineering',
        'position': 'Senior Lecturer',
        'job_type': 'full-time',
        'description': '''We are seeking an experienced and dedicated Senior Lecturer in Computer Science to join our dynamic department. 

The successful candidate will:
• Lead undergraduate and postgraduate teaching in core computer science areas
• Conduct research in their field of expertise
• Supervise student projects and thesis work
• Contribute to curriculum development and course design
• Mentor junior academic staff

Requirements:
• PhD in Computer Science or related field
• Minimum 5 years of teaching experience at university level
• Strong research record with publications in peer-reviewed journals
• Excellent communication and leadership skills''',
        'requirements': '''• PhD in Computer Science or equivalent
• Publication record in indexed journals
• Experience with student supervision
• Ability to teach in English and French preferred
• Strong interpersonal and team collaboration skills''',
        'salary_min': 5000,
        'salary_max': 7000,
        'currency': 'USD',
        'deadline': date.today() + timedelta(days=30),
        'is_active': True,
    },
    {
        'title': 'Librarian - Digital Resources',
        'slug': 'librarian-digital-resources',
        'department': 'Library Services',
        'position': 'Librarian',
        'job_type': 'full-time',
        'description': '''The University Library is seeking a dynamic Librarian to manage our digital resources and online services.

Responsibilities:
• Manage digital library collections and platforms
• Provide support for distance and online learning
• Train staff and users on digital resources
• Develop and maintain library web presence
• Coordinate with academic departments on digital services

You will work with modern library management systems and emerging technologies.''',
        'requirements': '''• Master's degree in Library Science or Information Management
• Experience with library management systems
• Knowledge of digital repositories and e-resources
• Strong customer service skills
• Technical aptitude and problem-solving ability''',
        'salary_min': 3500,
        'salary_max': 4500,
        'currency': 'USD',
        'deadline': date.today() + timedelta(days=25),
        'is_active': True,
    },
    {
        'title': 'Research Assistant (Biology)',
        'slug': 'research-assistant-biology',
        'department': 'Sciences',
        'position': 'Research Assistant',
        'job_type': 'contract',
        'description': '''A Research Assistant position is available in the Department of Biological Sciences for a 12-month contract.

The position involves:
• Supporting ongoing research projects in molecular biology
• Laboratory work and data collection
• Literature review and documentation
• Assisting with research publications
• Potential for field work

This is an excellent opportunity for early-career scientists to gain research experience.''',
        'requirements': '''• Bachelor's degree in Biology or related field
• Basic laboratory skills
• Ability to follow detailed protocols
• Good written and verbal communication
• Willingness to learn new techniques''',
        'salary_min': 2000,
        'salary_max': 2500,
        'currency': 'USD',
        'deadline': date.today() + timedelta(days=20),
        'is_active': True,
    },
]

for job_data in jobs_data:
    job, created = JobPosting.objects.get_or_create(
        slug=job_data['slug'],
        defaults=job_data
    )
    if created:
        print(f"✓ Job Posting created: {job.title}")
    else:
        print(f"✓ Job Posting exists: {job.title}")

print("\n✅ Job Postings seeding completed!")
print(f"   • Total Job Postings: {JobPosting.objects.count()}")
print(f"   • Open Positions: {JobPosting.objects.filter(is_active=True).count()}")
print(f"\nAccess at: http://localhost:8000/admin/jobs/")
