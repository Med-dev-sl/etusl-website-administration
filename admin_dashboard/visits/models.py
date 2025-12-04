from django.db import models
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class VisitRequest(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_REQUEST_INFO = 'REQUEST_INFO'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_REQUEST_INFO, 'Requested Info'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visit_requests'
    )
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='visits')
    reason = models.TextField(help_text='Reason for the visit (provided by user or secretary)')
    created_at = models.DateTimeField(auto_now_add=True)

    # If a secretary created the request on behalf of a user
    created_by_secretary = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='created_visits'
    )

    # Head response fields
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_PENDING)
    head_note = models.TextField(blank=True, help_text='Optional note from head when approving/rejecting')
    responded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='responded_visits'
    )
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"VisitRequest #{self.pk} — {self.requester} -> {self.department} ({self.status})"
