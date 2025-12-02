from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class MaintenanceTeam(models.Model):
    """Maintenance team/department structure"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    head_technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='teams_headed')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Maintenance Teams'
        ordering = ['name']

    def __str__(self):
        return self.name


class Technician(models.Model):
    """Technician profiles with specializations"""
    SPECIALIZATION_CHOICES = [
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('hvac', 'HVAC/Cooling'),
        ('it', 'IT/Computing'),
        ('mechanical', 'Mechanical'),
        ('civil', 'Civil/Building'),
        ('general', 'General Maintenance'),
        ('laboratory', 'Laboratory Equipment'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='technician_profile')
    team = models.ForeignKey(MaintenanceTeam, on_delete=models.SET_NULL, null=True, related_name='technicians')
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES, default='general')
    license_number = models.CharField(max_length=50, blank=True, help_text='Professional license/certification')
    license_expiry = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Technicians'
        ordering = ['user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_specialization_display()}"


class MaintenanceRequest(models.Model):
    """Maintenance requests from staff/users"""
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent - 24 hours'),
        ('high', 'High - 3 days'),
        ('medium', 'Medium - 1 week'),
        ('low', 'Low - As available'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('acknowledged', 'Acknowledged'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    request_id = models.CharField(max_length=50, unique=True, editable=False)
    requester = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance_requests')
    
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, null=True, blank=True, help_text='Asset needing maintenance')
    location_description = models.CharField(max_length=255, help_text='Location if not asset-specific')
    
    title = models.CharField(max_length=255)
    description = models.TextField(help_text='Detailed description of issue/problem')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    requested_date = models.DateTimeField(auto_now_add=True)
    target_completion_date = models.DateField(null=True, blank=True)
    
    assigned_to = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_requests')
    assigned_date = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True, help_text='Staff notes/additional info')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Maintenance Request'
        verbose_name_plural = 'Maintenance Requests'
        ordering = ['-requested_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_to']),
        ]

    def save(self, *args, **kwargs):
        if not self.request_id:
            import uuid
            self.request_id = f"MR-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_id} - {self.title}"


class MaintenanceWorkOrder(models.Model):
    """Work orders created from maintenance requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    work_order_id = models.CharField(max_length=50, unique=True, editable=False)
    maintenance_request = models.OneToOneField(MaintenanceRequest, on_delete=models.CASCADE, related_name='work_order')
    
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, related_name='work_orders')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_work_orders', help_text='Supervising staff member')
    
    scheduled_date = models.DateField()
    scheduled_start_time = models.TimeField()
    scheduled_end_time = models.TimeField()
    
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    work_description = models.TextField(blank=True, help_text='Detailed work to be performed')
    materials_required = models.TextField(blank=True, help_text='List of materials/parts needed')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Maintenance Work Order'
        verbose_name_plural = 'Maintenance Work Orders'
        ordering = ['-scheduled_date']

    def save(self, *args, **kwargs):
        if not self.work_order_id:
            import uuid
            self.work_order_id = f"WO-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.work_order_id} - {self.technician}"


class MaintenanceCompletion(models.Model):
    """Record of completed maintenance work"""
    work_order = models.OneToOneField(MaintenanceWorkOrder, on_delete=models.CASCADE, related_name='completion_record')
    
    completion_date = models.DateTimeField(auto_now_add=True)
    work_performed = models.TextField(help_text='Detailed description of work completed')
    
    materials_used = models.TextField(blank=True, help_text='Materials/parts actually used')
    parts_replaced = models.TextField(blank=True, help_text='List of replaced parts with part numbers')
    
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(Decimal('0.1'))])
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    parts_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0'))
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    
    asset_condition_after = models.CharField(max_length=50, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ], default='good')
    
    notes = models.TextField(blank=True, help_text='Additional notes or recommendations')
    follow_up_needed = models.BooleanField(default=False)
    follow_up_notes = models.TextField(blank=True)
    
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance_completions')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Maintenance Completion'
        verbose_name_plural = 'Maintenance Completions'
        ordering = ['-completion_date']

    def save(self, *args, **kwargs):
        if self.labor_cost and self.parts_cost is not None:
            self.total_cost = self.labor_cost + self.parts_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.work_order.work_order_id} - Completed"


class MaintenanceSignature(models.Model):
    """Digital signatures for maintenance work acceptance/completion"""
    SIGNATURE_TYPE_CHOICES = [
        ('technician_start', 'Technician - Work Start'),
        ('technician_end', 'Technician - Work Completion'),
        ('receiver_acceptance', 'Receiver - Work Acceptance'),
        ('supervisor_approval', 'Supervisor - Approval'),
        ('quality_check', 'QA Inspector - Quality Check'),
    ]

    work_order = models.ForeignKey(MaintenanceWorkOrder, on_delete=models.CASCADE, related_name='signatures')
    
    signature_type = models.CharField(max_length=25, choices=SIGNATURE_TYPE_CHOICES)
    signer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance_signatures')
    
    signature_data = models.TextField(help_text='Base64 encoded digital signature image')
    signature_timestamp = models.DateTimeField(auto_now_add=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.CharField(max_length=255, blank=True, help_text='Device used for signing')
    
    comments = models.TextField(blank=True)
    
    is_valid = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Maintenance Signature'
        verbose_name_plural = 'Maintenance Signatures'
        ordering = ['-signature_timestamp']
        unique_together = [('work_order', 'signature_type')]

    def __str__(self):
        return f"{self.work_order.work_order_id} - {self.get_signature_type_display()}"


class MaintenanceSchedule(models.Model):
    """Preventive maintenance schedules"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi-annual', 'Semi-annual'),
        ('annual', 'Annual'),
        ('bi-annual', 'Bi-annual'),
        ('as_needed', 'As Needed'),
    ]

    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, related_name='maintenance_schedules')
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    last_performed = models.DateField(null=True, blank=True)
    next_due_date = models.DateField()
    
    assigned_team = models.ForeignKey(MaintenanceTeam, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_duration_hours = models.DecimalField(max_digits=5, decimal_places=1)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Maintenance Schedule'
        verbose_name_plural = 'Maintenance Schedules'
        ordering = ['next_due_date']

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.title}"


class MaintenanceMetrics(models.Model):
    """Track maintenance KPIs and metrics"""
    month = models.DateField(help_text='First day of the month')
    
    total_requests = models.IntegerField(default=0)
    completed_requests = models.IntegerField(default=0)
    average_completion_time_days = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    emergency_requests = models.IntegerField(default=0)
    scheduled_maintenance_completed = models.IntegerField(default=0)
    
    total_maintenance_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'))
    total_labor_hours = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0'))
    
    downtime_hours = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0'))
    asset_availability_percent = models.DecimalField(
        max_digits=5, decimal_places=2, 
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))],
        null=True, blank=True
    )
    
    repeat_maintenance_issues = models.IntegerField(default=0, help_text='Same asset maintained multiple times')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Maintenance Metrics'
        verbose_name_plural = 'Maintenance Metrics'
        ordering = ['-month']
        unique_together = ['month']

    def __str__(self):
        return f"Metrics - {self.month.strftime('%B %Y')}"


class MaintenanceHistory(models.Model):
    """Complete maintenance history for audit trail"""
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE, related_name='maintenance_history')
    work_order = models.ForeignKey(MaintenanceWorkOrder, on_delete=models.SET_NULL, null=True, blank=True)
    
    maintenance_date = models.DateField()
    work_description = models.TextField()
    
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True)
    supervisor = models.CharField(max_length=255, blank=True)
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    spare_parts_used = models.TextField(blank=True)
    asset_condition_before = models.CharField(max_length=50, blank=True)
    asset_condition_after = models.CharField(max_length=50, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Maintenance History'
        verbose_name_plural = 'Maintenance Histories'
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"{self.asset.asset_tag} - {self.maintenance_date}"
