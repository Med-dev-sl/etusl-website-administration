from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from datetime import date, timedelta
from jobs.models import JobPosting


class Command(BaseCommand):
    help = 'Seed job postings with proper admin change history'

    def handle(self, *args, **options):
        jobs_data = [
            {
                'title': 'Senior Lecturer in Computer Science',
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
            },
            {
                'title': 'Librarian - Digital Resources',
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
            },
            {
                'title': 'Research Assistant (Biology)',
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
            },
        ]

        content_type = ContentType.objects.get_for_model(JobPosting)

        for job_data in jobs_data:
            job_posting, created = JobPosting.objects.get_or_create(
                slug=slugify(job_data['title']),
                defaults={
                    'title': job_data['title'],
                    'department': job_data['department'],
                    'position': job_data['position'],
                    'job_type': job_data['job_type'],
                    'description': job_data['description'],
                    'requirements': job_data['requirements'],
                    'salary_min': job_data['salary_min'],
                    'salary_max': job_data['salary_max'],
                    'currency': job_data['currency'],
                    'deadline': job_data['deadline'],
                    'is_active': True,
                }
            )

            if created:
                # Create admin change history entry
                LogEntry.objects.create(
                    content_type=content_type,
                    object_id=job_posting.id,
                    object_repr=str(job_posting),
                    action_flag=ADDITION,
                    change_message='Initial creation via seed script',
                    user_id=1,  # Assumes superuser exists with id=1
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Job Posting created: {job_posting.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⊘ Job Posting already exists: {job_posting.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('✅ Job Postings seeding completed with change history!')
        )
