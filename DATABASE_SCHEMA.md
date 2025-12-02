# Database Schema & ER Diagram

## Entity-Relationship Model

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           UNIVERSITY CMS DATABASE                               │
└─────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │   auth.User      │
                              ├──────────────────┤
                              │ id               │
                              │ username         │
                              │ email            │
                              │ password         │
                              └────────┬─────────┘
                                       │ 1:1
                                       ├──────────┬──────────┬──────────┐
                                       │          │          │          │
                     ┌─────────────────▼─┐  ┌────▼────────┐ │ ┌────────▼──────┐
                     │ users.Profile      │  │ academics.  │ │ │ admissions.   │
                     ├────────────────────┤  │ Faculty     │ │ │ Applicant     │
                     │ id                 │  ├─────────────┤ │ ├───────────────┤
                     │ user (1:1)         │  │ id          │ │ │ id            │
                     │ bio                │  │ user (1:1)  │ │ │ first_name    │
                     └────────────────────┘  │ full_name   │ │ │ last_name     │
                                             │ email       │ │ │ email         │
                                             │ phone       │ │ │ program (FK)  │
                                             └──────┬──────┘ │ │ status        │
                                                    │        │ │ admission_... │
                                                    │1       │ │ (FK)          │
                                        ┌───────────▼──┐    │ └───────────────┘
                                        │ academics.   │    │
                                        │ Department   │    │
                                        ├──────────────┤    │
                                        │ id           │    │
                                        │ name (U)     │    │
                                        │ slug (U)     │    │
                                        │ description  │    │
                                        │ head_of_...  │    │
                                        │ email        │    │
                                        │ phone        │    │
                                        │ office_...   │    │
                                        │ image        │    │
                                        └───────┬──────┘    │
                                                │ 1         │
                                        ┌───────▼──────┐    │
                                        │ academics.   │    │
                                        │ Program      │    │
                                        ├──────────────┤    │
                                        │ id           │    │
                                        │ department   ├─────┤
                                        │ (FK)         │    │
                                        │ name         │    │
                                        │ slug (U)     │    │
                                        │ level        │    │
                                        │ description  │    │
                                        │ duration_... │    │
                                        │ tuition_fee  │    │
                                        │ entry_req... │    │
                                        │ career_...   │    │
                                        │ program_...  │    │
                                        │ is_active    │    │
                                        └───────┬──────┘    │
                                                │ 1         │
                                        ┌───────▼──────┐    │
                                        │ academics.   ├────┘
                                        │ Course       │
                                        ├──────────────┤
                                        │ id           │
                                        │ program (FK) │
                                        │ code (U)     │
                                        │ title        │
                                        │ description  │
                                        │ credits      │
                                        │ semester     │
                                        │ instructor   │
                                        │ is_required  │
                                        └──────────────┘

                                ┌──────────────────┐
                                │ admissions.      │
                                │ AdmissionCycle   │
                                ├──────────────────┤
                                │ id               │
                                │ year (U)         │
                                │ start_date       │
                                │ end_date         │
                                │ application_...  │
                                │ result_announce..│
                                │ is_active        │
                                │ description      │
                                └──────┬───────────┘
                                       │ 1
                          ┌────────────┴──────────────┐
                          │ 1                         │ 1
                    ┌─────▼────────────┐   ┌─────────▼──────────┐
                    │ admissions.      │   │ admissions.        │
                    │ Requirement      │   │ Applicant          │
                    ├──────────────────┤   ├────────────────────┤
                    │ id               │   │ id                 │
                    │ program (FK)     │   │ admission_cycle(FK)│
                    │ title            │   │ first_name         │
                    │ description      │   │ last_name          │
                    │ document_type    │   │ email (U)          │
                    │ is_mandatory     │   │ phone              │
                    └────────┬─────────┘   │ date_of_birth      │
                             │ 1           │ nationality        │
                             │      ┌──────┤ program (FK)       │
                             │      │      │ status             │
                    ┌────────▼──────┴──┐   │ gpa                │
                    │ admissions.      │   │ documents_uploaded │
                    │ UploadedDocument │   │ notes              │
                    ├──────────────────┤   └────────────────────┘
                    │ id               │
                    │ applicant (FK)   │
                    │ requirement (FK) │
                    │ document_file    │
                    │ uploaded_at      │
                    └──────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ OTHER CORE MODELS (NOT SHOWN FOR BREVITY)                        │
├──────────────────────────────────────────────────────────────────┤
│ • pages.Page         - Dynamic pages (About, Contact, etc.)     │
│ • news.NewsPost      - News & announcements                     │
│ • events.Event       - Events with dates and locations          │
│ • staff.StaffMember  - Basic staff info                         │
│ • media.MediaFile    - File uploads (images, docs, videos)     │
└──────────────────────────────────────────────────────────────────┘
```

## Key Relationships

### One-to-Many (1:N)
- **Department → Program** (one department has many programs)
- **Program → Course** (one program offers many courses)
- **Program → Applicant** (one program receives many applications)
- **AdmissionCycle → Applicant** (one cycle has many applicants)
- **Department → Faculty** (one department has many faculty)
- **Requirement → UploadedDocument** (one requirement can have many uploaded docs)

### One-to-One (1:1)
- **User ↔ Profile** (each user has one profile)
- **User ↔ Faculty** (each faculty member links to one user account)

### Unique Constraints
- Department.name, slug
- Program.slug
- Course.code (globally unique)
- Applicant.email

## Table Specifications

### academics.Department
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | int | PK | Auto-increment |
| name | varchar(255) | NOT NULL, UNIQUE | Department name |
| slug | slug | NOT NULL, UNIQUE | URL-friendly name |
| description | text | | Department overview |
| head_of_department | varchar(255) | | HOD name |
| email | email | | Contact email |
| phone | varchar(20) | | Contact phone |
| office_location | varchar(255) | | Office room/building |
| image | image | nullable | Department logo/image |
| created_at | datetime | auto_now_add | Creation timestamp |

### academics.Program
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | int | PK | Auto-increment |
| department_id | int | FK (Department) | Parent department |
| name | varchar(255) | NOT NULL | Program name |
| slug | slug | NOT NULL, UNIQUE | URL-friendly name |
| level | varchar(20) | choices | diploma/bachelors/masters/phd |
| description | text | | Program details |
| duration_months | int | | Course length |
| tuition_fee | decimal(10,2) | nullable | Annual/total fee |
| entry_requirements | text | | Admission criteria |
| career_prospects | text | | Future career paths |
| program_coordinator | varchar(255) | | Coordinator name |
| is_active | boolean | default=True | Active/inactive status |
| created_at | datetime | auto_now_add | Creation timestamp |

### academics.Course
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | int | PK | Auto-increment |
| program_id | int | FK (Program) | Parent program |
| code | varchar(10) | NOT NULL, UNIQUE | e.g., CS101 |
| title | varchar(255) | NOT NULL | Course name |
| description | text | | Course content |
| credits | int | default=3 | Credit hours |
| semester | int | | Semester offered |
| instructor | varchar(255) | | Instructor name |
| is_required | boolean | default=True | Mandatory/elective |
| created_at | datetime | auto_now_add | Creation timestamp |
| **Composite** | **Unique** | program_id + code | Unique per program |

### academics.Faculty
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | int | PK | Auto-increment |
| user_id | int | FK (User), nullable | Django user account |
| full_name | varchar(255) | NOT NULL | Faculty name |
| department_id | int | FK (Department), nullable | Department |
| title | varchar(255) | | Professor/Lecturer/etc |
| email | email | NOT NULL | Email address |
| phone | varchar(20) | | Phone number |
| office_room | varchar(100) | | Office location |
| specialization | varchar(255) | | Research/teaching specialty |
| bio | text | | Biography |
| photo | image | nullable | Profile photo |
| publications | text | | Research papers/achievements |
| created_at | datetime | auto_now_add | Creation timestamp |

### admissions.AdmissionCycle
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | int | PK | Auto-increment |
| year | int | NOT NULL, UNIQUE | e.g., 2025 |
| start_date | date | NOT NULL | Cycle start |
| end_date | date | NOT NULL | Cycle end |
| application_deadline | date | NOT NULL | Deadline |
| result_announcement_date | date | nullable | When results are published |
| is_active | boolean | default=True | Current cycle? |
| description | text | | Additional info |
| created_at | datetime | auto_now_add | Creation timestamp |

### admissions.Applicant
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | int | PK | Auto-increment |
| admission_cycle_id | int | FK (AdmissionCycle), nullable | Which cycle |
| first_name | varchar(255) | NOT NULL | First name |
| last_name | varchar(255) | NOT NULL | Last name |
| email | email | NOT NULL, UNIQUE | Email |
| phone | varchar(20) | NOT NULL | Phone |
| date_of_birth | date | NOT NULL | DOB |
| nationality | varchar(100) | | Citizenship |
| program_id | int | FK (Program), nullable | Applied program |
| status | varchar(20) | choices | draft/submitted/under_review/shortlisted/accepted/rejected/enrolled |
| gpa | decimal(3,2) | nullable | Entrance exam score |
| documents_uploaded | boolean | default=False | All docs uploaded? |
| notes | text | | Admin notes |
| applied_at | datetime | auto_now_add | Application date |
| updated_at | datetime | auto_now | Last update |

### admissions.Requirement
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | int | PK | Auto-increment |
| program_id | int | FK (Program) | Required for which program |
| title | varchar(255) | NOT NULL | Requirement name |
| description | text | NOT NULL | What's needed |
| document_type | varchar(100) | | e.g., PDF, Certificate |
| is_mandatory | boolean | default=True | Required/optional |
| created_at | datetime | auto_now_add | Creation timestamp |

### admissions.UploadedDocument
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | int | PK | Auto-increment |
| applicant_id | int | FK (Applicant) | Which applicant |
| requirement_id | int | FK (Requirement), nullable | Which requirement |
| document_file | file | NOT NULL | Uploaded file |
| uploaded_at | datetime | auto_now_add | Upload timestamp |

## Sample Data Seeds

See `seed_data.py` for adding sample departments, programs, and courses.

## Relationships Summary

```python
# Navigation examples:
dept = Department.objects.get(id=1)
dept.programs.all()              # All programs in department
dept.faculty.all()               # All faculty in department

program = Program.objects.get(id=1)
program.courses.all()            # All courses in program
program.applicants.all()         # All applicants for program
program.admission_requirements.all()  # Admission requirements

applicant = Applicant.objects.get(id=1)
applicant.documents.all()        # All documents uploaded
applicant.program                # The program applied to

cycle = AdmissionCycle.objects.get(id=1)
cycle.applicants.all()          # All applicants this cycle
```

## Design Decisions

1. **Foreign Keys & Cascading**
   - Department → Program: CASCADE (delete dept = delete programs)
   - Program → Applicant: SET_NULL (delete program ≠ delete applicant)
   - Requirement → UploadedDocument: CASCADE (delete requirement = delete documents)

2. **Unique Constraints**
   - Course codes are globally unique (not just per program) to simplify API
   - Applicant email is unique (one application per person per cycle)
   - Program slugs and Department slugs are globally unique for cleaner URLs

3. **Status Fields**
   - AdmissionCycle: `is_active` flag for determining current admission period
   - Applicant: `status` choices for tracking application workflow
   - Program: `is_active` flag for archiving old programs without deleting

4. **Image Handling**
   - All image uploads use `ImageField` (requires Pillow)
   - File storage is local in dev, AWS S3 in production

---

**Last Updated**: December 2, 2025  
**Schema Version**: 1.0
