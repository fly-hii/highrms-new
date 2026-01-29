"""
models.py

This module is used to register models for activity_monitoring app
"""

from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from attendance.models import AttendanceActivity
from base.horilla_company_manager import HorillaCompanyManager
from base.models import Company
from employee.models import Employee
from horilla.models import HorillaModel


class WorkSession(HorillaModel):
    """
    WorkSession model - Tracks a single work session from check-in to check-out
    """

    STATUS_CHOICES = [
        ("active", _("Active")),
        ("completed", _("Completed")),
    ]

    employee_id = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="work_sessions",
        verbose_name=_("Employee"),
    )
    attendance_activity = models.ForeignKey(
        AttendanceActivity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="work_session",
        verbose_name=_("Attendance Activity"),
    )
    attendance_date = models.DateField(
        verbose_name=_("Attendance Date"),
    )
    session_start = models.DateTimeField(
        verbose_name=_("Session Start"),
    )
    session_end = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Session End"),
    )
    total_active_seconds = models.IntegerField(
        default=0,
        verbose_name=_("Total Active Seconds"),
    )
    total_idle_seconds = models.IntegerField(
        default=0,
        verbose_name=_("Total Idle Seconds"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name=_("Status"),
    )
    session_token = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Session Token"),
    )
    token_expiry = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Token Expiry"),
    )
    objects = HorillaCompanyManager(
        related_company_field="employee_id__employee_work_info__company_id"
    )
    
    # Add company_filter as a class attribute to prevent AttributeError
    # This will be overridden by CompanyMiddleware if needed
    company_filter = None

    class Meta:
        """
        Meta class to add some additional options
        """

        ordering = ["-attendance_date", "-session_start"]
        indexes = [
            models.Index(fields=["employee_id", "attendance_date"]),
            models.Index(fields=["status"]),
            models.Index(fields=["session_token"]),
        ]
        verbose_name = _("Work Session")
        verbose_name_plural = _("Work Sessions")

    def __str__(self):
        return f"{self.employee_id} - {self.attendance_date} - {self.status}"

    def get_total_work_seconds(self):
        """
        Calculate total work time in seconds
        """
        return self.total_active_seconds + self.total_idle_seconds

    def get_productivity_percentage(self):
        """
        Calculate productivity percentage
        """
        total = self.get_total_work_seconds()
        if total == 0:
            return 0
        return (self.total_active_seconds / total) * 100


class ActivityLog(HorillaModel):
    """
    ActivityLog model - Logs domain-based activity during work sessions
    """

    work_session = models.ForeignKey(
        WorkSession,
        on_delete=models.CASCADE,
        related_name="activity_logs",
        verbose_name=_("Work Session"),
    )
    domain_name = models.CharField(
        max_length=255,
        verbose_name=_("Domain Name"),
    )
    active_seconds = models.IntegerField(
        default=0,
        verbose_name=_("Active Seconds"),
    )
    idle_seconds = models.IntegerField(
        default=0,
        verbose_name=_("Idle Seconds"),
    )
    is_allowed = models.BooleanField(
        default=True,
        verbose_name=_("Is Allowed Domain"),
    )
    timestamp_start = models.DateTimeField(
        verbose_name=_("Timestamp Start"),
    )
    timestamp_end = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Timestamp End"),
    )
    objects = HorillaCompanyManager(
        related_company_field="work_session__employee_id__employee_work_info__company_id"
    )
    
    # Add company_filter as a class attribute to prevent AttributeError
    company_filter = None

    class Meta:
        """
        Meta class to add some additional options
        """

        ordering = ["-timestamp_start"]
        indexes = [
            models.Index(fields=["work_session", "domain_name"]),
            models.Index(fields=["is_allowed"]),
        ]
        verbose_name = _("Activity Log")
        verbose_name_plural = _("Activity Logs")

    def __str__(self):
        return f"{self.work_session.employee_id} - {self.domain_name} - {self.timestamp_start}"


class ExtensionHeartbeat(HorillaModel):
    """
    ExtensionHeartbeat model - Tracks heartbeat pings from browser extension
    """

    STATUS_CHOICES = [
        ("active", _("Active")),
        ("idle", _("Idle")),
    ]

    work_session = models.ForeignKey(
        WorkSession,
        on_delete=models.CASCADE,
        related_name="heartbeats",
        verbose_name=_("Work Session"),
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Timestamp"),
    )
    domain_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Domain Name"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name=_("Status"),
    )
    objects = HorillaCompanyManager(
        related_company_field="work_session__employee_id__employee_work_info__company_id"
    )
    
    # Add company_filter as a class attribute to prevent AttributeError
    company_filter = None

    class Meta:
        """
        Meta class to add some additional options
        """

        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["work_session", "timestamp"]),
            models.Index(fields=["status"]),
        ]
        verbose_name = _("Extension Heartbeat")
        verbose_name_plural = _("Extension Heartbeats")

    def __str__(self):
        return f"{self.work_session.employee_id} - {self.timestamp} - {self.status}"


class AllowedDomain(HorillaModel):
    """
    AllowedDomain model - Maintains list of allowed domains per company
    """

    company_id = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="allowed_domains",
        verbose_name=_("Company"),
    )
    domain_name = models.CharField(
        max_length=255,
        verbose_name=_("Domain Name"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )
    objects = HorillaCompanyManager()

    class Meta:
        """
        Meta class to add some additional options
        """

        ordering = ["company_id", "domain_name"]
        unique_together = [["company_id", "domain_name"]]
        verbose_name = _("Allowed Domain")
        verbose_name_plural = _("Allowed Domains")

    def __str__(self):
        company_name = self.company_id.company if self.company_id else "All Companies"
        return f"{company_name} - {self.domain_name}"


class DailyEmployeeReport(HorillaModel):
    """
    DailyEmployeeReport model - Denormalized summary table for fast reporting
    """

    employee_id = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="daily_activity_reports",
        verbose_name=_("Employee"),
    )
    work_session = models.OneToOneField(
        WorkSession,
        on_delete=models.CASCADE,
        related_name="daily_report",
        verbose_name=_("Work Session"),
    )
    report_date = models.DateField(
        verbose_name=_("Report Date"),
    )
    total_work_time = models.IntegerField(
        default=0,
        verbose_name=_("Total Work Time (seconds)"),
    )
    productive_time = models.IntegerField(
        default=0,
        verbose_name=_("Productive Time (seconds)"),
    )
    idle_time = models.IntegerField(
        default=0,
        verbose_name=_("Idle Time (seconds)"),
    )
    violation_count = models.IntegerField(
        default=0,
        verbose_name=_("Policy Violation Count"),
    )
    top_domains = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Top Domains"),
    )
    objects = HorillaCompanyManager(
        related_company_field="employee_id__employee_work_info__company_id"
    )
    
    # Add company_filter as a class attribute to prevent AttributeError
    company_filter = None

    class Meta:
        """
        Meta class to add some additional options
        """

        ordering = ["-report_date", "employee_id"]
        indexes = [
            models.Index(fields=["employee_id", "report_date"]),
            models.Index(fields=["report_date"]),
        ]
        unique_together = [["employee_id", "report_date"]]
        verbose_name = _("Daily Employee Report")
        verbose_name_plural = _("Daily Employee Reports")

    def __str__(self):
        return f"{self.employee_id} - {self.report_date}"

    def get_productivity_percentage(self):
        """
        Calculate productivity percentage
        """
        if self.total_work_time == 0:
            return 0
        return (self.productive_time / self.total_work_time) * 100

