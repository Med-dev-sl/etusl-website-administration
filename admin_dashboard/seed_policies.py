#!/usr/bin/env python
"""
Seed University Policies and Strategic Plans
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')
django.setup()

from policies.models import UniversityPolicy, StrategicPlan

# Create sample policies
policies_data = [
    {
        'title': 'Academic Integrity Policy',
        'slug': 'academic-integrity-policy',
        'category': 'academic',
        'description': 'Guidelines and standards for academic honesty and integrity',
        'content': '''This policy outlines the university's commitment to academic integrity and the expectations for all members of the academic community.

Key Points:
• All work submitted must be original and the work of the student submitting it
• Plagiarism, cheating, and academic dishonesty are serious violations
• Proper citation and attribution of sources is mandatory
• Students must acknowledge collaboration and seek permission where required
• Violations will result in disciplinary action

The university community is built on trust and mutual respect. Academic integrity is fundamental to our educational mission.''',
        'is_active': True,
    },
    {
        'title': 'Data Protection and Privacy Policy',
        'slug': 'data-protection-privacy-policy',
        'category': 'it',
        'description': 'Protection of personal data and privacy of students and staff',
        'content': '''ETUSL is committed to protecting the personal data and privacy of all stakeholders.

Principles:
• Personal data is collected only for legitimate purposes
• Data is processed transparently and lawfully
• Individuals have the right to access their personal data
• Data is kept secure and protected from unauthorized access
• Data retention follows legal and institutional guidelines

All staff and students must comply with data protection regulations and university policies.''',
        'is_active': True,
    },
]

for policy_data in policies_data:
    policy, created = UniversityPolicy.objects.get_or_create(
        slug=policy_data['slug'],
        defaults=policy_data
    )
    if created:
        print(f"✓ Policy created: {policy.title}")
    else:
        print(f"✓ Policy exists: {policy.title}")

# Create strategic plan
strategic_plan, created = StrategicPlan.objects.get_or_create(
    year=2025,
    slug='strategic-plan-2025-2030',
    defaults={
        'title': 'Strategic Plan 2025-2030',
        'duration_years': 5,
        'description': 'ETUSL Strategic Direction for 2025-2030',
        'vision': 'To be a leading university of choice for academic excellence, innovation, and development of socially responsible graduates.',
        'mission': 'To provide quality education, foster research and innovation, and contribute to societal development through teaching, learning, and community engagement.',
        'strategic_goals': '''1. Academic Excellence
   - Enhance teaching and learning quality
   - Expand academic programs and offerings
   - Strengthen faculty development

2. Research and Innovation
   - Promote research culture and funding
   - Support innovation and entrepreneurship
   - Build research infrastructure

3. Student Development
   - Improve student support services
   - Expand extracurricular opportunities
   - Develop leadership and soft skills

4. Infrastructure and Technology
   - Upgrade campus facilities
   - Enhance digital learning platforms
   - Improve ICT infrastructure

5. Community Engagement
   - Strengthen stakeholder partnerships
   - Expand community service programs
   - Increase industry collaboration''',
        'is_active': True,
    }
)

if created:
    print(f"✓ Strategic Plan created: {strategic_plan.title} ({strategic_plan.year}-{strategic_plan.year + strategic_plan.duration_years - 1})")
else:
    print(f"✓ Strategic Plan exists: {strategic_plan.title}")

print("\n✅ Policies and Strategic Plans seeding completed!")
print(f"   • Policies: {UniversityPolicy.objects.count()}")
print(f"   • Strategic Plans: {StrategicPlan.objects.count()}")
print(f"\nAccess at: http://localhost:8000/admin/policies/")
