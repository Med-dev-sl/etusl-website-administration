from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Department, VisitRequest
from .serializers import DepartmentSerializer, VisitRequestSerializer


class IsHeadOrSecretary(permissions.BasePermission):
    """Placeholder permission: refine to your project's roles."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class VisitRequestViewSet(viewsets.ModelViewSet):
    queryset = VisitRequest.objects.all().select_related('requester', 'department')
    serializer_class = VisitRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # If a secretary creates on behalf of someone, they can set created_by_secretary
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        # Secretaries and heads may want to see all; normal users see their own
        if user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(requester=user)

    @action(detail=True, methods=['post'], url_path='respond')
    def respond(self, request, pk=None):
        """Head (or staff) can approve/reject/request-info with a note."""
        visit = self.get_object()
        if not request.user.is_staff:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        status_value = request.data.get('status')
        note = request.data.get('note', '')

        if status_value not in dict(VisitRequest.STATUS_CHOICES):
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        visit.status = status_value
        visit.head_note = note
        visit.responded_by = request.user
        visit.responded_at = timezone.now()
        visit.save()
        return Response(self.get_serializer(visit).data)
