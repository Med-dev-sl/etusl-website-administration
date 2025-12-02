#!/usr/bin/env python
"""
Seed Maintenance Management System data
"""
import os
import django
from datetime import date, datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')
django.setup()

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from maintenance.models import (
    MaintenanceTeam, Technician, MaintenanceRequest, MaintenanceWorkOrder,
    MaintenanceCompletion, MaintenanceSchedule, MaintenanceHistory
)
from assets.models import Asset

admin_user = User.objects.filter(username='ETUSLWEB001').first() or User.objects.filter(is_superuser=True).first()

print("=" * 70)
print("SEEDING MAINTENANCE MANAGEMENT SYSTEM DATA")
print("=" * 70)

# ===== Maintenance Teams =====
teams_data = [
    {
        'name': 'Electrical & Power Systems',
        'description': 'Manages electrical systems, power distribution, generators',
        'phone': '+232-76-123456',
        'email': 'electrical@etusl.edu'
    },
    {
        'name': 'HVAC & Facilities',
        'description': 'Climate control, ventilation, water systems',
        'phone': '+232-76-123457',
        'email': 'hvac@etusl.edu'
    },
    {
        'name': 'IT & Computing Equipment',
        'description': 'Computers, servers, networking, printers',
        'phone': '+232-76-123458',
        'email': 'it-support@etusl.edu'
    },
    {
        'name': 'Laboratory & Scientific Equipment',
        'description': 'Lab instruments, scientific equipment, calibration',
        'phone': '+232-76-123459',
        'email': 'lab-maintenance@etusl.edu'
    },
    {
        'name': 'General Maintenance',
        'description': 'Plumbing, general repairs, building maintenance',
        'phone': '+232-76-123460',
        'email': 'maintenance@etusl.edu'
    },
]

teams = {}
for team_data in teams_data:
    team, created = MaintenanceTeam.objects.get_or_create(
        name=team_data['name'],
        defaults={
            'description': team_data['description'],
            'phone': team_data['phone'],
            'email': team_data['email'],
            'is_active': True,
        }
    )
    teams[team_data['name']] = team
    if created:
        print(f"✓ Maintenance Team created: {team.name}")

# ===== Technicians =====
# Create or find users for technicians
tech_users = []
tech_names = [
    ('Samuel', 'Conteh', 'samuel.conteh@etusl.edu', 'electrical'),
    ('Aisha', 'Sesay', 'aisha.sesay@etusl.edu', 'hvac'),
    ('James', 'Bangura', 'james.bangura@etusl.edu', 'it'),
    ('Maria', 'Koroma', 'maria.koroma@etusl.edu', 'laboratory'),
    ('David', 'Jalloh', 'david.jalloh@etusl.edu', 'general'),
]

spec_to_team = {
    'electrical': 'Electrical & Power Systems',
    'hvac': 'HVAC & Facilities',
    'it': 'IT & Computing Equipment',
    'laboratory': 'Laboratory & Scientific Equipment',
    'general': 'General Maintenance',
}

for first, last, email, spec in tech_names:
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': f'{first.lower()}.{last.lower()}',
            'first_name': first,
            'last_name': last,
        }
    )
    
    tech, created = Technician.objects.get_or_create(
        user=user,
        defaults={
            'team': teams[spec_to_team[spec]],
            'specialization': spec,
            'license_number': f'LIC-{first[0]}{last[0]}-2024-001',
            'license_expiry': date(2027, 12, 31),
            'phone': f'+232-76-{7700000 + hash(email) % 100000}',
            'is_active': True,
        }
    )
    
    if created:
        print(f"✓ Technician created: {user.get_full_name()} ({spec})")
    tech_users.append(tech)

# ===== Maintenance Requests =====
assets_list = list(Asset.objects.all()[:4])

requests_data = [
    {
        'title': 'Server overheating - high temperature alerts',
        'description': 'Dell PowerEdge server in server room reporting high CPU temperatures (75°C). Urgent attention needed.',
        'priority': 'urgent',
        'asset': assets_list[0] if assets_list else None,
        'status': 'acknowledged',
        'assigned_to': tech_users[2] if len(tech_users) > 2 else None,
        'days_offset': -7,
    },
    {
        'title': 'Microscope focus adjustment needed',
        'description': 'Zeiss microscope focus mechanism not holding position. Needs recalibration.',
        'priority': 'high',
        'asset': assets_list[2] if len(assets_list) > 2 else None,
        'status': 'scheduled',
        'assigned_to': tech_users[3] if len(tech_users) > 3 else None,
        'days_offset': -3,
    },
    {
        'title': 'Printer jam and error lights',
        'description': 'HP printer showing paper jam error. Unable to clear through standard procedures.',
        'priority': 'medium',
        'asset': assets_list[1] if len(assets_list) > 1 else None,
        'status': 'submitted',
        'assigned_to': None,
        'days_offset': -1,
    },
    {
        'title': 'RFID gate system malfunction',
        'description': 'Library RFID gate not detecting book checkouts properly. Security gate opens intermittently.',
        'priority': 'high',
        'asset': assets_list[3] if len(assets_list) > 3 else None,
        'status': 'acknowledged',
        'assigned_to': tech_users[2] if len(tech_users) > 2 else None,
        'days_offset': -5,
    },
]

requests = []
for req_data in requests_data:
    req, created = MaintenanceRequest.objects.get_or_create(
        title=req_data['title'],
        requester=admin_user,
        defaults={
            'description': req_data['description'],
            'priority': req_data['priority'],
            'asset': req_data['asset'],
            'status': req_data['status'],
            'assigned_to': req_data['assigned_to'],
            'assigned_date': datetime.now() if req_data['assigned_to'] else None,
            'target_completion_date': date.today() + timedelta(days=7),
        }
    )
    
    if created:
        # Update request date for realism
        MaintenanceRequest.objects.filter(pk=req.pk).update(
            requested_date=datetime.now() - timedelta(days=req_data['days_offset'])
        )
        print(f"✓ Maintenance Request created: {req.request_id} - {req.title}")
    requests.append(req)

# ===== Maintenance Work Orders =====
for idx, req in enumerate(requests[:2]):
    if req.status in ['scheduled', 'acknowledged'] and req.assigned_to:
        wo, created = MaintenanceWorkOrder.objects.get_or_create(
            maintenance_request=req,
            defaults={
                'technician': req.assigned_to,
                'supervisor': admin_user,
                'scheduled_date': date.today() + timedelta(days=1),
                'scheduled_start_time': datetime.strptime('09:00', '%H:%M').time(),
                'scheduled_end_time': datetime.strptime('12:00', '%H:%M').time(),
                'status': 'scheduled',
                'work_description': f'Inspect and service {req.asset.name if req.asset else "equipment"}',
                'materials_required': 'Thermal paste, replacement parts as needed',
                'estimated_cost': Decimal('150.00'),
            }
        )
        
        if created:
            print(f"✓ Work Order created: {wo.work_order_id} - {wo.technician.user.get_full_name()}")

# ===== Maintenance Schedules =====
if assets_list:
    schedule_data = [
        {
            'asset': assets_list[0],
            'title': 'Quarterly Server Maintenance',
            'description': 'Full server check including cooling, backup systems, security patches',
            'frequency': 'quarterly',
            'next_due': date.today() + timedelta(days=30),
            'team': teams['Electrical & Power Systems'],
            'duration': Decimal('4.0'),
        },
        {
            'asset': assets_list[2],
            'title': 'Annual Microscope Calibration',
            'description': 'Complete optical calibration, lens cleaning, focus mechanism check',
            'frequency': 'annual',
            'next_due': date.today() + timedelta(days=60),
            'team': teams['Laboratory & Scientific Equipment'],
            'duration': Decimal('3.0'),
        },
    ]
    
    for sched_data in schedule_data:
        sched, created = MaintenanceSchedule.objects.get_or_create(
            asset=sched_data['asset'],
            title=sched_data['title'],
            defaults={
                'description': sched_data['description'],
                'frequency': sched_data['frequency'],
                'next_due_date': sched_data['next_due'],
                'assigned_team': sched_data['team'],
                'estimated_duration_hours': sched_data['duration'],
                'estimated_cost': Decimal('200.00'),
                'is_active': True,
            }
        )
        
        if created:
            print(f"✓ Maintenance Schedule created: {sched.asset.asset_tag} - {sched.title}")

# ===== Maintenance Completions =====
if requests:
    completed_wo = MaintenanceWorkOrder.objects.filter(status='scheduled').first()
    if completed_wo and not hasattr(completed_wo, 'completion_record'):
        comp, created = MaintenanceCompletion.objects.get_or_create(
            work_order=completed_wo,
            defaults={
                'work_performed': 'Cleaned cooling system, replaced thermal paste, verified temperature sensors',
                'materials_used': 'Arctic Silver thermal paste, compression fitting',
                'parts_replaced': 'Thermal paste application',
                'hours_worked': Decimal('2.5'),
                'labor_cost': Decimal('150.00'),
                'parts_cost': Decimal('50.00'),
                'total_cost': Decimal('200.00'),
                'asset_condition_after': 'good',
                'completed_by': admin_user,
                'notes': 'Server temperatures now stabilized. Scheduled for next quarter check.',
            }
        )
        
        if created:
            print(f"✓ Maintenance Completion recorded: {completed_wo.work_order_id}")

# ===== Maintenance History =====
if assets_list:
    history_data = [
        {
            'asset': assets_list[1],
            'date': date.today() - timedelta(days=90),
            'description': 'Replaced printer drum and fuser assembly',
            'tech': tech_users[2] if len(tech_users) > 2 else None,
            'duration': Decimal('1.5'),
            'cost': Decimal('180.00'),
        },
        {
            'asset': assets_list[0],
            'date': date.today() - timedelta(days=180),
            'description': 'Quarterly server maintenance and backup verification',
            'tech': tech_users[0] if len(tech_users) > 0 else None,
            'duration': Decimal('4.0'),
            'cost': Decimal('300.00'),
        },
    ]
    
    for hist_data in history_data:
        hist, created = MaintenanceHistory.objects.get_or_create(
            asset=hist_data['asset'],
            maintenance_date=hist_data['date'],
            defaults={
                'work_description': hist_data['description'],
                'technician': hist_data['tech'],
                'duration_hours': hist_data['duration'],
                'cost': hist_data['cost'],
                'asset_condition_before': 'fair',
                'asset_condition_after': 'good',
                'notes': 'Routine maintenance completed successfully',
            }
        )
        
        if created:
            print(f"✓ Maintenance History created: {hist_data['asset'].asset_tag} - {hist_data['date']}")

print("\n" + "=" * 70)
print("✅ MAINTENANCE SYSTEM SEEDING COMPLETED!")
print("=" * 70)
print(f"• Maintenance Teams: {MaintenanceTeam.objects.count()}")
print(f"• Technicians: {Technician.objects.count()}")
print(f"• Maintenance Requests: {MaintenanceRequest.objects.count()}")
print(f"• Work Orders: {MaintenanceWorkOrder.objects.count()}")
print(f"• Completions: {MaintenanceCompletion.objects.count()}")
print(f"• Schedules: {MaintenanceSchedule.objects.count()}")
print(f"• History Records: {MaintenanceHistory.objects.count()}")
print("=" * 70)
