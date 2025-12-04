from rest_framework import serializers
from .models import Department, VisitRequest


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class VisitRequestSerializer(serializers.ModelSerializer):
    requester_username = serializers.ReadOnlyField(source='requester.username')
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = VisitRequest
        fields = [
            'id', 'requester', 'requester_username', 'department', 'department_name',
            'reason', 'created_by_secretary', 'status', 'head_note', 'responded_by', 'responded_at', 'created_at'
        ]
        read_only_fields = ('responded_at', 'created_at')

    def validate(self, data):
        # Ensure reason is provided
        reason = data.get('reason') or self.instance and self.instance.reason
        if not reason:
            raise serializers.ValidationError({'reason': 'A reason is required for visit requests.'})
        return data
