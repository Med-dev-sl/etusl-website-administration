"""
Sample data seeding script for ETUSL CMS.
Run with: python manage.py shell < seed_data.py
"""

from academics.models import Department, Program, Course, Faculty
from admissions.models import AdmissionCycle, Requirement, Applicant
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

print("Creating sample data...")

# Clear existing data (optional)
# Department.objects.all().delete()
# Program.objects.all().delete()
# AdmissionCycle.objects.all().delete()

# ============================================================================
# DEPARTMENTS
# ============================================================================

engineering, created = Department.objects.get_or_create(
    name='Engineering',
    defaults={
        'slug': 'engineering',
        'description': 'Faculty of Engineering - Innovative Solutions',
        'head_of_department': 'Dr. James Mensah',
        'email': 'eng@university.edu',
        'phone': '+234-123-456',
        'office_location': 'Engineering Building, Block A'
    }
)
print(f"✓ Department: {engineering.name} {'(created)' if created else '(exists)'}")

sciences, created = Department.objects.get_or_create(
    name='Sciences',
    defaults={
        'slug': 'sciences',
        'description': 'Faculty of Sciences - Advancing Knowledge',
        'head_of_department': 'Prof. Ama Boateng',
        'email': 'sci@university.edu',
        'phone': '+234-123-457',
        'office_location': 'Science Complex, Wing B'
    }
)
print(f"✓ Department: {sciences.name} {'(created)' if created else '(exists)'}")

arts, created = Department.objects.get_or_create(
    name='Arts & Humanities',
    defaults={
        'slug': 'arts-humanities',
        'description': 'Faculty of Arts & Humanities - Preserving Culture',
        'head_of_department': 'Dr. Kwesi Owusu',
        'email': 'arts@university.edu',
        'phone': '+234-123-458',
        'office_location': 'Arts Building, Floor 3'
    }
)
print(f"✓ Department: {arts.name} {'(created)' if created else '(exists)'}")

# ============================================================================
# PROGRAMS
# ============================================================================

bsc_cs, created = Program.objects.get_or_create(
    name='BSc Computer Science',
    defaults={
        'slug': 'bsc-computer-science',
        'department': engineering,
        'level': 'bachelors',
        'description': 'A 4-year program covering software development, algorithms, databases, and AI.',
        'duration_months': 48,
        'tuition_fee': 5000.00,
        'entry_requirements': 'A-Level or equivalent with passes in Math and Physics',
        'career_prospects': 'Software Engineer, Data Scientist, Systems Architect',
        'program_coordinator': 'Dr. Mensah Kwaku',
        'is_active': True
    }
)
print(f"✓ Program: {bsc_cs.name} {'(created)' if created else '(exists)'}")

bsc_physics, created = Program.objects.get_or_create(
    name='BSc Physics',
    defaults={
        'slug': 'bsc-physics',
        'department': sciences,
        'level': 'bachelors',
        'description': 'A 4-year program in Physics covering classical mechanics, thermodynamics, quantum physics.',
        'duration_months': 48,
        'tuition_fee': 3500.00,
        'entry_requirements': 'A-Level or equivalent with passes in Math and Physics',
        'career_prospects': 'Research Scientist, Educator, Energy Specialist',
        'program_coordinator': 'Prof. Boateng Ama',
        'is_active': True
    }
)
print(f"✓ Program: {bsc_physics.name} {'(created)' if created else '(exists)'}")

ba_english, created = Program.objects.get_or_create(
    name='BA English Literature',
    defaults={
        'slug': 'ba-english-literature',
        'department': arts,
        'level': 'bachelors',
        'description': 'A 4-year program covering British, American, and African literature.',
        'duration_months': 48,
        'tuition_fee': 2500.00,
        'entry_requirements': 'A-Level or equivalent with passes in English and History',
        'career_prospects': 'Writer, Editor, Teacher, Journalist',
        'program_coordinator': 'Dr. Owusu Kwesi',
        'is_active': True
    }
)
print(f"✓ Program: {ba_english.name} {'(created)' if created else '(exists)'}")

# ============================================================================
# COURSES
# ============================================================================

courses_data = [
    # Computer Science courses
    ('CS101', 'Introduction to Computer Science', bsc_cs, 1, 3, True),
    ('CS102', 'Programming Fundamentals (Python)', bsc_cs, 1, 3, True),
    ('CS201', 'Data Structures', bsc_cs, 2, 3, True),
    ('CS202', 'Database Design', bsc_cs, 2, 3, True),
    ('CS301', 'Web Development', bsc_cs, 3, 3, False),
    ('CS401', 'Artificial Intelligence', bsc_cs, 4, 3, False),
    
    # Physics courses
    ('PH101', 'Classical Mechanics', bsc_physics, 1, 4, True),
    ('PH102', 'Calculus for Physics', bsc_physics, 1, 4, True),
    ('PH201', 'Thermodynamics', bsc_physics, 2, 4, True),
    ('PH301', 'Quantum Physics', bsc_physics, 3, 4, True),
    
    # English courses
    ('EN101', 'Shakespeare & Early Modern Literature', ba_english, 1, 3, True),
    ('EN102', 'Writing Skills', ba_english, 1, 3, True),
    ('EN201', 'American Literature', ba_english, 2, 3, True),
    ('EN301', 'African Literature', ba_english, 3, 3, True),
]

for code, title, program, semester, credits, is_required in courses_data:
    course, created = Course.objects.get_or_create(
        code=code,
        defaults={
            'program': program,
            'title': title,
            'semester': semester,
            'credits': credits,
            'is_required': is_required,
            'description': f'{title} for {program.name}'
        }
    )
    if created:
        print(f"✓ Course: {code} - {title}")

# ============================================================================
# FACULTY MEMBERS
# ============================================================================

faculty_data = [
    ('Dr. Kofi Mensah', engineering, 'Professor', 'kofi.mensah@university.edu', 'Software Engineering'),
    ('Dr. Ama Boateng', sciences, 'Associate Professor', 'ama.boateng@university.edu', 'Quantum Physics'),
    ('Dr. Kwesi Owusu', arts, 'Lecturer', 'kwesi.owusu@university.edu', 'British Literature'),
    ('Dr. Abena Asante', engineering, 'Lecturer', 'abena.asante@university.edu', 'Database Systems'),
]

for full_name, dept, title, email, spec in faculty_data:
    faculty, created = Faculty.objects.get_or_create(
        email=email,
        defaults={
            'full_name': full_name,
            'department': dept,
            'title': title,
            'specialization': spec,
            'bio': f'{title} specializing in {spec}',
            'office_room': f'{dept.name} - Room {hash(email) % 100 + 100}'
        }
    )
    if created:
        print(f"✓ Faculty: {full_name}")

# ============================================================================
# ADMISSION CYCLES
# ============================================================================

current_year = datetime.now().year
cycle, created = AdmissionCycle.objects.get_or_create(
    year=current_year,
    defaults={
        'start_date': date(current_year, 1, 15),
        'end_date': date(current_year, 12, 31),
        'application_deadline': date(current_year, 4, 30),
        'result_announcement_date': date(current_year, 7, 15),
        'is_active': True,
        'description': f'{current_year} Main Admission Cycle'
    }
)
print(f"✓ Admission Cycle: {cycle.year} {'(created)' if created else '(exists)'}")

# ============================================================================
# ADMISSION REQUIREMENTS
# ============================================================================

requirements = [
    (bsc_cs, 'High School Certificate', 'Certified copy of O-Level or equivalent', 'PDF'),
    (bsc_cs, 'Birth Certificate', 'Official birth certificate', 'PDF/Scanned'),
    (bsc_cs, 'National ID', 'Photocopy of valid national ID', 'PDF'),
    (bsc_physics, 'High School Certificate', 'Certified copy of O-Level', 'PDF'),
    (ba_english, 'High School Certificate', 'Certified copy of O-Level', 'PDF'),
]

for program, title, desc, doc_type in requirements:
    req, created = Requirement.objects.get_or_create(
        program=program,
        title=title,
        defaults={
            'description': desc,
            'document_type': doc_type,
            'is_mandatory': True
        }
    )
    if created:
        print(f"✓ Requirement: {program.name} → {title}")

# ============================================================================
# SAMPLE APPLICANTS
# ============================================================================

applicants_data = [
    ('John', 'Mensah', 'john.mensah@email.com', '0541234567', date(2004, 5, 15), 'Ghana', bsc_cs, 'submitted', 3.8),
    ('Ama', 'Boateng', 'ama.boateng@email.com', '0541234568', date(2004, 8, 22), 'Ghana', bsc_cs, 'under_review', 3.6),
    ('Kwesi', 'Owusu', 'kwesi.owusu@email.com', '0541234569', date(2005, 1, 10), 'Ghana', bsc_physics, 'submitted', 3.5),
    ('Abena', 'Asante', 'abena.asante@email.com', '0541234570', date(2004, 12, 3), 'Ghana', ba_english, 'draft', 3.2),
]

for first_name, last_name, email, phone, dob, nationality, program, status, gpa in applicants_data:
    applicant, created = Applicant.objects.get_or_create(
        email=email,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'date_of_birth': dob,
            'nationality': nationality,
            'admission_cycle': cycle,
            'program': program,
            'status': status,
            'gpa': gpa,
            'documents_uploaded': status in ['submitted', 'under_review', 'shortlisted', 'accepted']
        }
    )
    if created:
        print(f"✓ Applicant: {first_name} {last_name} → {program.name}")

print("\n✅ Sample data seeding completed!")
print(f"\nSummary:")
print(f"  • Departments: {Department.objects.count()}")
print(f"  • Programs: {Program.objects.count()}")
print(f"  • Courses: {Course.objects.count()}")
print(f"  • Faculty: {Faculty.objects.count()}")
print(f"  • Admission Cycles: {AdmissionCycle.objects.count()}")
print(f"  • Requirements: {Requirement.objects.count()}")
print(f"  • Applicants: {Applicant.objects.count()}")
