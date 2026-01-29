"""
signals.py

This module handles signals for activity monitoring integration with attendance system
"""

import secrets
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from activity_monitoring.models import WorkSession
from attendance.models import AttendanceActivity
from django.utils.timezone import make_aware


@receiver(post_save, sender=AttendanceActivity)
def create_work_session_on_checkin(sender, instance, created, **kwargs):
    """
    Create WorkSession when employee checks in (clock_in is set, clock_out is None)
    """
    # Only create session on check-in (when clock_in exists but clock_out is None)
    if instance.clock_in and not instance.clock_out:
        # Check if a work session already exists for this attendance activity
        existing_session = WorkSession.objects.filter(
            attendance_activity=instance, status="active"
        ).first()

        if not existing_session:
            # Generate session token
            session_token = secrets.token_urlsafe(32)
            token_expiry = timezone.now() + timedelta(hours=12)  # Token valid for 12 hours

            # Create work session
            # Ensure timezone-aware datetime
            session_start = timezone.now()
            if timezone.is_naive(session_start):
                session_start = make_aware(session_start)
            
            work_session = WorkSession.objects.create(
                employee_id=instance.employee_id,
                attendance_activity=instance,
                attendance_date=instance.attendance_date or timezone.now().date(),
                session_start=session_start,
                status="active",
                session_token=session_token,
                token_expiry=token_expiry,
            )


@receiver(post_save, sender=AttendanceActivity)
def complete_work_session_on_checkout(sender, instance, **kwargs):
    """
    Complete WorkSession when employee checks out (clock_out is set)
    """
    # Only process if clock_out is set
    if instance.clock_out:
        # Find active work session for this attendance activity
        work_session = WorkSession.objects.filter(
            attendance_activity=instance, status="active"
        ).first()

        if work_session:
            # Update session end time
            work_session.session_end = timezone.now()
            work_session.status = "completed"
            work_session.save()

            # Import here to avoid circular imports
            from activity_monitoring.methods.utils import (
                generate_daily_report,
                update_work_session_on_checkout,
            )

            # Update work session statistics
            update_work_session_on_checkout(work_session)

            # Generate daily report
            generate_daily_report(work_session)

