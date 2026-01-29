"""
api/views.py

API views for browser extension communication
"""

import logging
import secrets
from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from activity_monitoring.methods.utils import (
    check_domain_allowed,
    extract_domain_from_url,
)
from activity_monitoring.models import ActivityLog, ExtensionHeartbeat, WorkSession
from activity_monitoring.serializers import (
    ActivityLogSerializer,
    BatchActivityLogSerializer,
    HeartbeatSerializer,
    SessionStatusSerializer,
    SessionTokenResponseSerializer,
)
from attendance.models import AttendanceActivity
from employee.models import Employee

logger = logging.getLogger(__name__)


class SessionTokenView(APIView):
    """
    API endpoint to generate session token on check-in
    POST /api/activity-monitoring/session/token/
    """

    permission_classes = [IsAuthenticated]
    # Use SessionAuthentication to allow session-based auth from browser extension
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        """
        Generate session token for authenticated employee who is checked in
        """
        try:
            employee = request.user.employee_get
        except AttributeError:
            return Response(
                {"error": "Employee not found for this user. Please ensure you are logged in."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Error getting employee: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Check if employee is currently checked in
        active_attendance = AttendanceActivity.objects.filter(
            employee_id=employee, clock_out__isnull=True
        ).order_by("-clock_in").first()

        if not active_attendance:
            return Response(
                {
                    "error": "Employee is not checked in. Please check in via the attendance system first.",
                    "employee_id": employee.id,
                    "employee_name": employee.get_full_name()
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if work session already exists
        work_session = WorkSession.objects.filter(
            attendance_activity=active_attendance, status="active"
        ).first()

        if not work_session:
            # Create new work session
            session_token = secrets.token_urlsafe(32)
            token_expiry = timezone.now() + timedelta(hours=12)

            work_session = WorkSession.objects.create(
                employee_id=employee,
                attendance_activity=active_attendance,
                attendance_date=active_attendance.attendance_date or timezone.now().date(),
                session_start=timezone.now(),
                status="active",
                session_token=session_token,
                token_expiry=token_expiry,
            )
        else:
            # Update token if expired or missing
            if not work_session.session_token or (
                work_session.token_expiry and work_session.token_expiry < timezone.now()
            ):
                work_session.session_token = secrets.token_urlsafe(32)
                work_session.token_expiry = timezone.now() + timedelta(hours=12)
                work_session.save()

        serializer = SessionTokenResponseSerializer(
            {
                "token": work_session.session_token,
                "session_id": work_session.id,
                "expiry_time": work_session.token_expiry,
                "employee_id": employee.id,
            }
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class HeartbeatView(APIView):
    """
    API endpoint to receive heartbeat pings from browser extension
    POST /api/activity-monitoring/heartbeat/
    """

    def post(self, request):
        """
        Process heartbeat from extension
        """
        serializer = HeartbeatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["token"]
        domain_name = serializer.validated_data.get("domain_name", "")
        heartbeat_status = serializer.validated_data["status"]

        # Validate token and get work session
        try:
            work_session = WorkSession.objects.get(
                session_token=token, status="active", token_expiry__gt=timezone.now()
            )
        except WorkSession.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Create heartbeat record
        ExtensionHeartbeat.objects.create(
            work_session=work_session,
            domain_name=domain_name,
            status=heartbeat_status,
        )

        # Heartbeat only marks status, does NOT add time
        # Time is tracked via ActivityLog entries from the extension
        # No need to update work_session counters here

        logger.info(
            f"Heartbeat received for session {work_session.id}, "
            f"domain: {domain_name}, status: {heartbeat_status}"
        )

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class ActivityLogView(APIView):
    """
    API endpoint to log activity from browser extension
    POST /api/activity-monitoring/activity-log/
    """

    authentication_classes = []  # No authentication required, token-based
    permission_classes = []  # No permission required, token-based

    def post(self, request):
        """
        Log activity from extension
        """
        serializer = ActivityLogSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["token"]
        domain_name = serializer.validated_data["domain_name"]
        active_seconds = serializer.validated_data["active_seconds"]
        idle_seconds = serializer.validated_data["idle_seconds"]
        is_allowed_flag = serializer.validated_data["is_allowed"]

        # Validate token and get work session
        try:
            work_session = WorkSession.objects.get(
                session_token=token, status="active", token_expiry__gt=timezone.now()
            )
        except WorkSession.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        # Check if domain is actually allowed (server-side validation)
        employee = work_session.employee_id
        # Normalize domain name before checking
        from activity_monitoring.methods.utils import normalize_domain
        normalized_domain = normalize_domain(domain_name)
        is_allowed = check_domain_allowed(normalized_domain, employee)

        # Validate timestamps if provided
        timestamp_start = serializer.validated_data.get("timestamp_start")
        timestamp_end = serializer.validated_data.get("timestamp_end")
        
        # If timestamps not provided, calculate from current time
        if not timestamp_start:
            timestamp_start = timezone.now() - timedelta(seconds=active_seconds + idle_seconds)
        if not timestamp_end:
            timestamp_end = timezone.now()
        
        # Validate timestamp order
        if timestamp_start >= timestamp_end:
            return Response(
                {"error": "timestamp_start must be before timestamp_end"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate time range is reasonable (not negative, not too large - max 8 hours)
        total_seconds = (timestamp_end - timestamp_start).total_seconds()
        if total_seconds < 0 or total_seconds > 28800:  # 8 hours max
            return Response(
                {"error": "Invalid time range"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create activity log (use normalized domain)
        ActivityLog.objects.create(
            work_session=work_session,
            domain_name=normalized_domain,
            active_seconds=active_seconds,
            idle_seconds=idle_seconds,
            is_allowed=is_allowed,
            timestamp_start=timestamp_start,
            timestamp_end=timestamp_end,
        )

        # Update work session totals (will be recalculated on checkout)
        work_session.total_active_seconds += active_seconds
        work_session.total_idle_seconds += idle_seconds
        work_session.save()

        logger.info(
            f"Activity log created for session {work_session.id}, "
            f"domain: {domain_name}, active: {active_seconds}s, idle: {idle_seconds}s, "
            f"allowed: {is_allowed}"
        )

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class BatchActivityLogView(APIView):
    """
    API endpoint to log multiple activities in batch
    POST /api/activity-monitoring/activity-logs/batch/
    """

    authentication_classes = []  # No authentication required, token-based
    permission_classes = []  # No permission required, token-based

    def post(self, request):
        """
        Log multiple activities from extension in batch
        """
        serializer = BatchActivityLogSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["token"]
        logs = serializer.validated_data["logs"]

        # Validate token and get work session
        try:
            work_session = WorkSession.objects.get(
                session_token=token, status="active", token_expiry__gt=timezone.now()
            )
        except WorkSession.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        employee = work_session.employee_id
        created_count = 0
        errors = []

        # Process each log in batch
        for log_data in logs:
            try:
                domain_name = log_data["domain_name"]
                active_seconds = log_data["active_seconds"]
                idle_seconds = log_data["idle_seconds"]
                is_allowed_flag = log_data.get("is_allowed", True)
                timestamp_start = log_data.get("timestamp_start")
                timestamp_end = log_data.get("timestamp_end")

                # Normalize domain name before checking
                from activity_monitoring.methods.utils import normalize_domain
                normalized_domain = normalize_domain(domain_name)
                
                # Check if domain is actually allowed (server-side validation)
                is_allowed = check_domain_allowed(normalized_domain, employee)

                # Validate timestamps
                if not timestamp_start:
                    timestamp_start = timezone.now() - timedelta(seconds=active_seconds + idle_seconds)
                if not timestamp_end:
                    timestamp_end = timezone.now()

                # Validate timestamp order
                if timestamp_start >= timestamp_end:
                    errors.append(f"Invalid timestamps for {domain_name}")
                    continue

                # Validate time range
                total_seconds = (timestamp_end - timestamp_start).total_seconds()
                if total_seconds < 0 or total_seconds > 28800:  # 8 hours max
                    errors.append(f"Invalid time range for {domain_name}")
                    continue

                # Create activity log (use normalized domain)
                ActivityLog.objects.create(
                    work_session=work_session,
                    domain_name=normalized_domain,
                    active_seconds=active_seconds,
                    idle_seconds=idle_seconds,
                    is_allowed=is_allowed,
                    timestamp_start=timestamp_start,
                    timestamp_end=timestamp_end,
                )

                # Update work session totals
                work_session.total_active_seconds += active_seconds
                work_session.total_idle_seconds += idle_seconds
                created_count += 1

            except Exception as e:
                errors.append(f"Error processing log for {log_data.get('domain_name', 'unknown')}: {str(e)}")

        # Save work session with updated totals
        work_session.save()

        logger.info(
            f"Batch activity logs processed for session {work_session.id}, "
            f"created: {created_count}/{len(logs)}, errors: {len(errors)}"
        )

        response_data = {
            "status": "success",
            "created": created_count,
            "total": len(logs),
        }
        
        if errors:
            response_data["errors"] = errors
            logger.warning(f"Errors in batch processing: {errors}")

        return Response(response_data, status=status.HTTP_200_OK)


class SessionStatusView(APIView):
    """
    API endpoint to get current session status
    GET /api/activity-monitoring/session/status/?token=<token>
    """

    authentication_classes = []  # No authentication required, token-based
    permission_classes = []  # No permission required, token-based

    def get(self, request):
        """
        Get current session status
        """
        token = request.query_params.get("token")
        if not token:
            return Response(
                {"error": "Token parameter required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            work_session = WorkSession.objects.get(
                session_token=token, status="active", token_expiry__gt=timezone.now()
            )
        except WorkSession.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = SessionStatusSerializer(
            {
                "session_id": work_session.id,
                "status": work_session.status,
                "employee_id": work_session.employee_id.id,
                "session_start": work_session.session_start,
                "total_active_seconds": work_session.total_active_seconds,
                "total_idle_seconds": work_session.total_idle_seconds,
            }
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

