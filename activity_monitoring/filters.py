"""
filters.py

Django filters for activity monitoring
"""

import django_filters
from django import forms

from activity_monitoring.models import DailyEmployeeReport, WorkSession
from employee.models import Employee


class WorkSessionFilter(django_filters.FilterSet):
    """
    WorkSessionFilter
    """

    employee_id = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={"class": "oh-select oh-select-2"}),
    )
    attendance_date = django_filters.DateFilter(
        field_name="attendance_date",
        lookup_expr="exact",
        widget=forms.DateInput(attrs={"type": "date", "class": "oh-input"}),
    )
    attendance_date_from = django_filters.DateFilter(
        field_name="attendance_date",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date", "class": "oh-input"}),
    )
    attendance_date_to = django_filters.DateFilter(
        field_name="attendance_date",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date", "class": "oh-input"}),
    )
    status = django_filters.ChoiceFilter(
        choices=WorkSession.STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "oh-select oh-select-2"}),
    )

    class Meta:
        model = WorkSession
        fields = ["employee_id", "attendance_date", "status"]


class DailyEmployeeReportFilter(django_filters.FilterSet):
    """
    DailyEmployeeReportFilter
    """

    employee_id = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={"class": "oh-select oh-select-2"}),
    )
    report_date = django_filters.DateFilter(
        field_name="report_date",
        lookup_expr="exact",
        widget=forms.DateInput(attrs={"type": "date", "class": "oh-input"}),
    )
    report_date_from = django_filters.DateFilter(
        field_name="report_date",
        lookup_expr="gte",
        widget=forms.DateInput(attrs={"type": "date", "class": "oh-input"}),
    )
    report_date_to = django_filters.DateFilter(
        field_name="report_date",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={"type": "date", "class": "oh-input"}),
    )

    class Meta:
        model = DailyEmployeeReport
        fields = ["employee_id", "report_date"]

