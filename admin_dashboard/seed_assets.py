#!/usr/bin/env python
"""
Seed Asset Register data with sample assets, inventory, and movements
"""
import os
import django
from datetime import date, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_dashboard.settings')
django.setup()

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from assets.models import (
    AssetCategory, AssetLocation, Asset, AssetMovement,
    InventoryItem, InventoryTransaction, MaintenanceRecord
)

# Get or create superuser for audit trail
admin_user = User.objects.filter(username='ETUSLWEB001').first() or User.objects.filter(is_superuser=True).first()

print("=" * 60)
print("SEEDING ASSET REGISTER DATA")
print("=" * 60)

# ===== Asset Categories =====
categories_data = [
    {
        'name': 'Computing & IT',
        'description': 'Computers, servers, networking equipment, peripherals'
    },
    {
        'name': 'Laboratory Equipment',
        'description': 'Scientific instruments, microscopes, spectrometers'
    },
    {
        'name': 'Furniture & Fixtures',
        'description': 'Desks, chairs, cabinets, shelving'
    },
    {
        'name': 'Office Equipment',
        'description': 'Printers, copiers, scanners, projectors'
    },
    {
        'name': 'Library Equipment',
        'description': 'RFID systems, circulation desks, shelving'
    },
    {
        'name': 'Facilities & Infrastructure',
        'description': 'HVAC, generators, water systems'
    },
]

categories = {}
for cat_data in categories_data:
    cat, created = AssetCategory.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    categories[cat_data['name']] = cat
    if created:
        print(f"✓ Asset Category created: {cat.name}")

# ===== Asset Locations =====
locations_data = [
    {'name': 'Server Room', 'department': 'IT', 'description': 'Main data center'},
    {'name': 'Main Lab 1', 'department': 'Sciences', 'description': 'Biology laboratory'},
    {'name': 'Main Lab 2', 'department': 'Sciences', 'description': 'Chemistry laboratory'},
    {'name': 'Computer Lab A', 'department': 'Engineering', 'description': 'General computer lab'},
    {'name': 'Library Main Floor', 'department': 'Library', 'description': 'Main circulation area'},
    {'name': 'Rector\'s Office', 'department': 'Administration', 'description': 'Executive office'},
    {'name': 'Central Store', 'department': 'Logistics', 'description': 'Main inventory storage'},
]

locations = {}
for loc_data in locations_data:
    loc, created = AssetLocation.objects.get_or_create(
        name=loc_data['name'],
        department=loc_data['department'],
        defaults={'description': loc_data['description']}
    )
    locations[loc_data['name']] = loc
    if created:
        print(f"✓ Asset Location created: {loc.name} ({loc.department})")

# ===== Assets =====
assets_data = [
    {
        'asset_tag': 'ASSET-IT-001',
        'name': 'Dell PowerEdge R750 Server',
        'category': 'Computing & IT',
        'location': 'Server Room',
        'purchase_price': Decimal('15000.00'),
        'acquisition_date': date(2022, 3, 15),
        'warranty_expiry': date(2027, 3, 15),
        'assigned_to': None,
        'status': 'active',
        'condition': 'excellent',
        'serial_number': 'SRV-2022-001'
    },
    {
        'asset_tag': 'ASSET-IT-002',
        'name': 'HP LaserJet Pro Printer M404n',
        'category': 'Office Equipment',
        'location': 'Rector\'s Office',
        'purchase_price': Decimal('1200.00'),
        'acquisition_date': date(2023, 6, 1),
        'warranty_expiry': date(2025, 6, 1),
        'assigned_to': None,
        'status': 'active',
        'condition': 'good',
        'serial_number': 'PRN-2023-001'
    },
    {
        'asset_tag': 'ASSET-LAB-001',
        'name': 'Zeiss Microscope - Optical',
        'category': 'Laboratory Equipment',
        'location': 'Main Lab 1',
        'purchase_price': Decimal('8500.00'),
        'acquisition_date': date(2021, 8, 20),
        'warranty_expiry': date(2026, 8, 20),
        'assigned_to': None,
        'status': 'active',
        'condition': 'excellent',
        'serial_number': 'MICRO-2021-001'
    },
    {
        'asset_tag': 'ASSET-LAB-002',
        'name': 'Spectrophotometer UV-Vis',
        'category': 'Laboratory Equipment',
        'location': 'Main Lab 2',
        'purchase_price': Decimal('5200.00'),
        'acquisition_date': date(2023, 1, 10),
        'warranty_expiry': date(2026, 1, 10),
        'assigned_to': None,
        'status': 'active',
        'condition': 'good',
        'serial_number': 'SPEC-2023-001'
    },
    {
        'asset_tag': 'ASSET-FUR-001',
        'name': 'Office Desk with Drawers (Beech)',
        'category': 'Furniture & Fixtures',
        'location': 'Computer Lab A',
        'purchase_price': Decimal('350.00'),
        'acquisition_date': date(2022, 9, 5),
        'warranty_expiry': None,
        'assigned_to': None,
        'status': 'active',
        'condition': 'good',
        'serial_number': 'FUR-2022-001'
    },
    {
        'asset_tag': 'ASSET-LIB-001',
        'name': 'RFID Gate System',
        'category': 'Library Equipment',
        'location': 'Library Main Floor',
        'purchase_price': Decimal('12000.00'),
        'acquisition_date': date(2022, 11, 30),
        'warranty_expiry': date(2025, 11, 30),
        'assigned_to': None,
        'status': 'active',
        'condition': 'good',
        'serial_number': 'RFID-2022-001'
    },
]

content_type = ContentType.objects.get_for_model(Asset)
for asset_data in assets_data:
    asset, created = Asset.objects.get_or_create(
        asset_tag=asset_data['asset_tag'],
        defaults={
            'name': asset_data['name'],
            'category': categories[asset_data['category']],
            'purchase_price': asset_data['purchase_price'],
            'current_value': asset_data['purchase_price'],
            'currency': 'USD',
            'acquisition_date': asset_data['acquisition_date'],
            'warranty_expiry': asset_data['warranty_expiry'],
            'current_location': locations[asset_data['location']],
            'assigned_to': asset_data['assigned_to'],
            'status': asset_data['status'],
            'condition': asset_data['condition'],
            'serial_number': asset_data['serial_number'],
            'created_by': admin_user,
        }
    )
    if created:
        # Create audit trail
        LogEntry.objects.create(
            content_type=content_type,
            object_id=asset.id,
            object_repr=str(asset),
            action_flag=ADDITION,
            change_message='Initial asset registration',
            user=admin_user,
        )
        print(f"✓ Asset created: {asset.asset_tag} - {asset.name}")

# ===== Inventory Items =====
inventory_data = [
    {
        'item_code': 'INV-PAPER-001',
        'name': 'A4 Paper (500 sheets)',
        'category': 'Office Equipment',
        'quantity_on_hand': 250,
        'reorder_level': 50,
        'reorder_quantity': 100,
        'unit': 'reams',
        'unit_cost': Decimal('8.50'),
        'storage_location': 'Central Store',
        'supplier': 'Staples Office Supplies',
        'last_restocked': date.today()
    },
    {
        'item_code': 'INV-TONER-001',
        'name': 'Toner Cartridge (Black)',
        'category': 'Office Equipment',
        'quantity_on_hand': 15,
        'reorder_level': 5,
        'reorder_quantity': 12,
        'unit': 'pieces',
        'unit_cost': Decimal('65.00'),
        'storage_location': 'Central Store',
        'supplier': 'HP Direct',
        'last_restocked': date.today()
    },
    {
        'item_code': 'INV-CHEM-001',
        'name': 'Sodium Hydroxide (NaOH) 1M Solution',
        'category': 'Laboratory Equipment',
        'quantity_on_hand': 8,
        'reorder_level': 3,
        'reorder_quantity': 10,
        'unit': 'liters',
        'unit_cost': Decimal('45.00'),
        'storage_location': 'Main Lab 2',
        'supplier': 'Sigma-Aldrich',
        'last_restocked': date(2025, 11, 15)
    },
    {
        'item_code': 'INV-GLASS-001',
        'name': 'Lab Beaker Set (500ml)',
        'category': 'Laboratory Equipment',
        'quantity_on_hand': 12,
        'reorder_level': 5,
        'reorder_quantity': 10,
        'unit': 'sets',
        'unit_cost': Decimal('35.00'),
        'storage_location': 'Main Lab 1',
        'supplier': 'Scientific Equipment Ltd',
        'last_restocked': date(2025, 10, 1)
    },
    {
        'item_code': 'INV-PEN-001',
        'name': 'Ballpoint Pens (Black)',
        'category': 'Office Equipment',
        'quantity_on_hand': 500,
        'reorder_level': 100,
        'reorder_quantity': 250,
        'unit': 'pieces',
        'unit_cost': Decimal('0.50'),
        'storage_location': 'Central Store',
        'supplier': 'Statex Ltd',
        'last_restocked': date.today()
    },
]

for inv_data in inventory_data:
    item, created = InventoryItem.objects.get_or_create(
        item_code=inv_data['item_code'],
        defaults={
            'name': inv_data['name'],
            'category': categories[inv_data['category']],
            'quantity_on_hand': inv_data['quantity_on_hand'],
            'reorder_level': inv_data['reorder_level'],
            'reorder_quantity': inv_data['reorder_quantity'],
            'unit': inv_data['unit'],
            'unit_cost': inv_data['unit_cost'],
            'currency': 'USD',
            'storage_location': locations[inv_data['storage_location']],
            'supplier': inv_data['supplier'],
            'last_restocked': inv_data['last_restocked'],
        }
    )
    if created:
        print(f"✓ Inventory Item created: {item.item_code} - {item.name}")

# ===== Asset Movements =====
movements_data = [
    {
        'asset_tag': 'ASSET-IT-001',
        'type': 'incoming',
        'from_loc': None,
        'to_loc': 'Server Room',
        'quantity': 1,
        'date_offset': -300,  # 300 days ago
        'reference': 'PO-2022-001'
    },
    {
        'asset_tag': 'ASSET-LAB-001',
        'type': 'incoming',
        'from_loc': None,
        'to_loc': 'Main Lab 1',
        'quantity': 1,
        'date_offset': -600,
        'reference': 'PO-2021-015'
    },
]

for mov_data in movements_data:
    asset = Asset.objects.get(asset_tag=mov_data['asset_tag'])
    movement, created = AssetMovement.objects.get_or_create(
        asset=asset,
        movement_type=mov_data['type'],
        reference_document=mov_data['reference'],
        defaults={
            'to_location': locations[mov_data['to_loc']] if mov_data['to_loc'] else None,
            'quantity': mov_data['quantity'],
            'recorded_by': admin_user,
        }
    )
    if created:
        print(f"✓ Asset Movement recorded: {asset.asset_tag} ({mov_data['type']})")

# ===== Inventory Transactions =====
trans_data = [
    {
        'item_code': 'INV-PAPER-001',
        'type': 'inbound',
        'quantity': 250,
        'reference': 'PO-2025-042',
        'date_offset': 0
    },
    {
        'item_code': 'INV-PEN-001',
        'type': 'outbound',
        'quantity': 100,
        'reference': 'REQ-2025-155',
        'date_offset': -5
    },
    {
        'item_code': 'INV-TONER-001',
        'type': 'outbound',
        'quantity': 3,
        'reference': 'REQ-2025-163',
        'date_offset': -2
    },
]

for trans_data in trans_data:
    item = InventoryItem.objects.get(item_code=trans_data['item_code'])
    trans, created = InventoryTransaction.objects.get_or_create(
        item=item,
        transaction_type=trans_data['type'],
        reference_document=trans_data['reference'],
        defaults={
            'quantity': trans_data['quantity'],
            'issued_by': admin_user,
        }
    )
    if created:
        print(f"✓ Inventory Transaction recorded: {item.item_code} ({trans_data['type']}, qty: {trans_data['quantity']})")

# ===== Maintenance Records =====
maintenance_data = [
    {
        'asset_tag': 'ASSET-IT-001',
        'title': 'Annual Server Maintenance',
        'description': 'Routine maintenance including cooling system check, backup verification, and security updates',
        'scheduled_date': date(2025, 12, 15),
        'status': 'scheduled'
    },
    {
        'asset_tag': 'ASSET-LAB-001',
        'title': 'Microscope Calibration',
        'description': 'Optical calibration and lens cleaning for precision measurement',
        'scheduled_date': date(2025, 12, 20),
        'status': 'scheduled'
    },
    {
        'asset_tag': 'ASSET-IT-002',
        'title': 'Printer Drum Replacement',
        'description': 'Replace worn printer drum unit and clean fuser assembly',
        'scheduled_date': date(2025, 12, 10),
        'completion_date': date(2025, 12, 10),
        'status': 'completed',
        'cost': Decimal('150.00')
    },
]

content_type = ContentType.objects.get_for_model(MaintenanceRecord)
for maint_data in maintenance_data:
    asset = Asset.objects.get(asset_tag=maint_data['asset_tag'])
    maint, created = MaintenanceRecord.objects.get_or_create(
        asset=asset,
        title=maint_data['title'],
        scheduled_date=maint_data['scheduled_date'],
        defaults={
            'description': maint_data['description'],
            'completion_date': maint_data.get('completion_date'),
            'status': maint_data['status'],
            'cost': maint_data.get('cost'),
            'currency': 'USD',
            'created_by': admin_user,
        }
    )
    if created:
        print(f"✓ Maintenance Record created: {asset.asset_tag} - {maint.title}")

print("\n" + "=" * 60)
print("✅ ASSET REGISTER SEEDING COMPLETED!")
print("=" * 60)
print(f"• Total Asset Categories: {AssetCategory.objects.count()}")
print(f"• Total Asset Locations: {AssetLocation.objects.count()}")
print(f"• Total Assets: {Asset.objects.count()}")
print(f"• Total Asset Movements: {AssetMovement.objects.count()}")
print(f"• Total Inventory Items: {InventoryItem.objects.count()}")
print(f"• Total Inventory Transactions: {InventoryTransaction.objects.count()}")
print(f"• Total Maintenance Records: {MaintenanceRecord.objects.count()}")
print("=" * 60)
