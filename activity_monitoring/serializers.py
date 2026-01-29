"""
serializers.py

Django REST Framework serializers for activity monitoring API
"""

from rest_framework import serializers

from activity_monitoring.models import ActivityLog, ExtensionHeartbeat, WorkSession


class WorkSessionSerializer(serializers.ModelSerializer):
    """
    WorkSessionSerializer
    """

    employee_name = serializers.CharField(source="employee_id.get_full_name", read_only=True)

    class Meta:
        model = WorkSession
        fields = [
            "id",
            "employee_id",
            "employee_name",
            "attendance_date",
            "session_start",
            "session_end",
            "status",
            "total_active_seconds",
            "total_idle_seconds",
            "session_token",
        ]
        read_only_fields = [
            "id",
            "session_start",
            "session_end",
            "total_active_seconds",
            "total_idle_seconds",
            "session_token",
        ]


class HeartbeatSerializer(serializers.Serializer):
    """
    HeartbeatSerializer for extension heartbeat requests
    """

    token = serializers.CharField(required=True)
    domain_name = serializers.CharField(required=True, allow_blank=True)
    status = serializers.ChoiceField(choices=["active", "idle"], required=True)


class ActivityLogSerializer(serializers.Serializer):
    """
    ActivityLogSerializer for extension activity log requests
    """

    token = serializers.CharField(required=True)
    domain_name = serializers.CharField(required=True)
    active_seconds = serializers.IntegerField(required=True, min_value=0)
    idle_seconds = serializers.IntegerField(required=True, min_value=0)
    is_allowed = serializers.BooleanField(required=True)
    timestamp_start = serializers.DateTimeField(required=False, allow_null=True)
    timestamp_end = serializers.DateTimeField(required=False, allow_null=True)


class BatchActivityLogItemSerializer(serializers.Serializer):
    """
    Serializer for individual log item in batch
    """
    
    domain_name = serializers.CharField(required=True)
    active_seconds = serializers.IntegerField(required=True, min_value=0)
    idle_seconds = serializers.IntegerField(required=True, min_value=0)
    timestamp_start = serializers.DateTimeField(required=False, allow_null=True)
    timestamp_end = serializers.DateTimeField(required=False, allow_null=True)
    is_allowed = serializers.BooleanField(required=False, default=True)


class BatchActivityLogSerializer(serializers.Serializer):
    """
    BatchActivityLogSerializer for batch activity log requests
    """
    
    token = serializers.CharField(required=True)
    logs = BatchActivityLogItemSerializer(many=True, required=True)


class SessionTokenResponseSerializer(serializers.Serializer):
    """
    SessionTokenResponseSerializer
    """

    token = serializers.CharField()
    session_id = serializers.IntegerField()
    expiry_time = serializers.DateTimeField()
    employee_id = serializers.IntegerField()


class SessionStatusSerializer(serializers.Serializer):
    """
    SessionStatusSerializer
    """

    session_id = serializers.IntegerField()
    status = serializers.CharField()
    employee_id = serializers.IntegerField()
    session_start = serializers.DateTimeField()
    total_active_seconds = serializers.IntegerField()
    total_idle_seconds = serializers.IntegerField()

