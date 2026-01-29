"""
admin.py

This module is used to register models in Django admin
"""

from django.contrib import admin

from activity_monitoring.models import (
    ActivityLog,
    AllowedDomain,
    DailyEmployeeReport,
    ExtensionHeartbeat,
    WorkSession,
)


@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    """
    WorkSessionAdmin
    """

    list_display = [
        "employee_id",
        "attendance_date",
        "session_start",
        "session_end",
        "status",
        "total_active_seconds",
        "total_idle_seconds",
    ]
    list_filter = ["status", "attendance_date"]
    search_fields = ["employee_id__employee_first_name", "employee_id__employee_last_name"]
    readonly_fields = ["session_start", "session_token", "token_expiry"]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """
    ActivityLogAdmin
    """

    list_display = [
        "work_session",
        "domain_name",
        "active_seconds",
        "idle_seconds",
        "is_allowed",
        "timestamp_start",
    ]
    list_filter = ["is_allowed", "timestamp_start"]
    search_fields = ["domain_name", "work_session__employee_id__employee_first_name"]


@admin.register(ExtensionHeartbeat)
class ExtensionHeartbeatAdmin(admin.ModelAdmin):
    """
    ExtensionHeartbeatAdmin
    """

    list_display = ["work_session", "timestamp", "domain_name", "status"]
    list_filter = ["status", "timestamp"]
    readonly_fields = ["timestamp"]


@admin.register(AllowedDomain)
class AllowedDomainAdmin(admin.ModelAdmin):
    """
    AllowedDomainAdmin
    """

    list_display = ["company_id", "domain_name", "is_active", "created_at"]
    list_filter = ["is_active", "company_id"]
    search_fields = ["domain_name"]


@admin.register(DailyEmployeeReport)
class DailyEmployeeReportAdmin(admin.ModelAdmin):
    """
    DailyEmployeeReportAdmin
    """

    list_display = [
        "employee_id",
        "report_date",
        "total_work_time",
        "productive_time",
        "idle_time",
        "violation_count",
    ]
    list_filter = ["report_date"]
    search_fields = ["employee_id__employee_first_name", "employee_id__employee_last_name"]
    readonly_fields = ["top_domains"]

