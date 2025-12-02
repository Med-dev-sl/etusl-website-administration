from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class AssetCategory(models.Model):
    """Categories for assets (Equipment, Furniture, IT, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Asset Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class AssetLocation(models.Model):
    """Departments, offices, labs where assets are located"""
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['department', 'name']

    def __str__(self):
        return f"{self.name} ({self.department})"


class Asset(models.Model):
    """Main Asset Register for tracking all university assets"""
    STATUS_CHOICES = [
        ('active', 'Active - In Use'),
        ('inactive', 'Inactive - Not in Use'),
        ('damaged', 'Damaged'),
        ('disposed', 'Disposed'),
        ('lost', 'Lost'),
        ('maintenance', 'Under Maintenance'),
    ]

    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('condemned', 'Condemned'),
    ]

    # Basic Information
    asset_tag = models.CharField(max_length=50, unique=True, help_text='Unique asset identifier')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    
    # Financial Information
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, help_text='Original purchase price')
    current_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='Current estimated value')
    currency = models.CharField(max_length=10, default='USD')
    
    # Lifecycle Information
    acquisition_date = models.DateField(help_text='Date when asset was acquired')
    warranty_expiry = models.DateField(null=True, blank=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'), help_text='Annual depreciation % (e.g., 10.00)')
    
    # Location & Assignment
    current_location = models.ForeignKey(AssetLocation, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text='Staff member responsible for this asset')
    
    # Status & Condition
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    
    # Maintenance & History
    last_maintenance_date = models.DateField(null=True, blank=True)
    maintenance_notes = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assets_created')

    class Meta:
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['asset_tag']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['current_location']),
        ]

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"

    def years_in_service(self):
        """Calculate years since acquisition"""
        from datetime import date
        if not self.acquisition_date:
            return 0
        delta = date.today() - self.acquisition_date
        return delta.days / 365.25

    def depreciated_value(self):
        """Calculate current depreciated value"""
        if self.acquisition_date:
            years = self.years_in_service()
            depreciated = self.purchase_price * ((100 - self.depreciation_rate) / 100) ** years
            return max(Decimal('0'), depreciated)
        return self.purchase_price


class AssetMovement(models.Model):
    """Track asset movements (incoming, outgoing, transfers)"""
    MOVEMENT_TYPE_CHOICES = [
        ('incoming', 'Incoming - New Asset'),
        ('outgoing', 'Outgoing - Disposal/Sale'),
        ('transfer', 'Transfer - Location Change'),
        ('return', 'Return - From User'),
        ('assignment', 'Assignment - To User'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    
    from_location = models.ForeignKey(AssetLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets_moved_from')
    to_location = models.ForeignKey(AssetLocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets_moved_to')
    
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets_from_user')
    to_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets_to_user')
    
    quantity = models.IntegerField(default=1, help_text='For consumables, number of items')
    notes = models.TextField(blank=True)
    reference_document = models.CharField(max_length=100, blank=True, help_text='PO, Invoice, Receipt number')
    
    movement_date = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='asset_movements_recorded')

    class Meta:
        verbose_name = 'Asset Movement'
        verbose_name_plural = 'Asset Movements'
        ordering = ['-movement_date']

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.get_movement_type_display()} ({self.movement_date.date()})"


class InventoryItem(models.Model):
    """Consumable items and supplies inventory"""
    UNIT_CHOICES = [
        ('pieces', 'Pieces'),
        ('boxes', 'Boxes'),
        ('reams', 'Reams'),
        ('liters', 'Liters'),
        ('kg', 'Kilograms'),
        ('meters', 'Meters'),
        ('sets', 'Sets'),
        ('rolls', 'Rolls'),
        ('other', 'Other'),
    ]

    item_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT)
    
    # Inventory Levels
    quantity_on_hand = models.IntegerField(default=0, help_text='Current quantity in stock')
    reorder_level = models.IntegerField(default=10, help_text='Minimum quantity before reorder')
    reorder_quantity = models.IntegerField(default=50, help_text='Quantity to order when below reorder level')
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pieces')
    
    # Financial
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    
    # Location
    storage_location = models.ForeignKey(AssetLocation, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    supplier = models.CharField(max_length=255, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_restocked = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.item_code} - {self.name}"

    def total_value(self):
        """Calculate total inventory value"""
        if not self.unit_cost:
            return Decimal('0')
        return self.quantity_on_hand * self.unit_cost

    def needs_reorder(self):
        """Check if item needs reordering"""
        return self.quantity_on_hand <= self.reorder_level


class InventoryTransaction(models.Model):
    """Track all inventory transactions (in, out, adjustments)"""
    TRANSACTION_TYPE_CHOICES = [
        ('inbound', 'Inbound - Received'),
        ('outbound', 'Outbound - Issued'),
        ('adjustment', 'Adjustment - Correction'),
        ('damage', 'Damage - Write-off'),
        ('return', 'Return - From User'),
    ]

    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    
    quantity = models.IntegerField()
    reference_document = models.CharField(max_length=100, blank=True, help_text='PO, Receipt, Requisition number')
    issued_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text='Who received the item')
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_issued')
    
    notes = models.TextField(blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Inventory Transaction'
        verbose_name_plural = 'Inventory Transactions'
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.item.item_code} - {self.get_transaction_type_display()} ({self.quantity} {self.item.unit})"


class MaintenanceRecord(models.Model):
    """Track maintenance and service records for assets"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    scheduled_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text='Technician responsible')
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance_records_created')

    class Meta:
        verbose_name = 'Maintenance Record'
        verbose_name_plural = 'Maintenance Records'
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.title}"
