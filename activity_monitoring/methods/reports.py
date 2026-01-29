"""
reports.py

Report generation functions for CSV/Excel exports
"""

import csv
from datetime import datetime

import pandas as pd
from django.http import HttpResponse

from activity_monitoring.models import ActivityLog, DailyEmployeeReport
from activity_monitoring.methods.utils import format_seconds_to_time


def export_daily_report_csv(date, employee_id=None):
    """
    Export daily report as CSV

    Args:
        date: Date object
        employee_id: Optional employee ID to filter

    Returns:
        HttpResponse with CSV file
    """
    if employee_id:
        reports = DailyEmployeeReport.objects.filter(
            report_date=date, employee_id=employee_id
        ).select_related("employee_id")
    else:
        reports = DailyEmployeeReport.objects.filter(report_date=date).select_related(
            "employee_id"
        )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="daily_report_{date}.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Employee Name",
            "Date",
            "Total Work Time",
            "Productive Time",
            "Idle Time",
            "Violations",
            "Productivity %",
        ]
    )

    for report in reports:
        writer.writerow(
            [
                report.employee_id.get_full_name(),
                report.report_date.strftime("%Y-%m-%d"),
                format_seconds_to_time(report.total_work_time),
                format_seconds_to_time(report.productive_time),
                format_seconds_to_time(report.idle_time),
                report.violation_count,
                f"{report.get_productivity_percentage():.2f}%",
            ]
        )

    return response


def export_employee_report_excel(employee_id, date_from, date_to):
    """
    Export employee-wise report as Excel

    Args:
        employee_id: Employee ID
        date_from: Start date
        date_to: End date

    Returns:
        HttpResponse with Excel file
    """
    reports = DailyEmployeeReport.objects.filter(
        employee_id=employee_id,
        report_date__gte=date_from,
        report_date__lte=date_to,
    ).select_related("employee_id")

    if not reports.exists():
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="employee_report_empty.xlsx"'
        return response

    # Prepare data for Excel
    data = {
        "Date": [],
        "Total Work Time": [],
        "Productive Time": [],
        "Idle Time": [],
        "Violations": [],
        "Productivity %": [],
    }

    for report in reports:
        # Use date only, not datetime
        data["Date"].append(report.report_date.strftime("%Y-%m-%d"))
        data["Total Work Time"].append(format_seconds_to_time(report.total_work_time))
        data["Productive Time"].append(format_seconds_to_time(report.productive_time))
        data["Idle Time"].append(format_seconds_to_time(report.idle_time))
        data["Violations"].append(report.violation_count)
        data["Productivity %"].append(f"{report.get_productivity_percentage():.2f}%")

    df = pd.DataFrame(data)

    response = HttpResponse(content_type="application/ms-excel")
    employee_name = reports.first().employee_id.get_full_name().replace(" ", "_")
    response["Content-Disposition"] = (
        f'attachment; filename="employee_report_{employee_name}_{date_from}_{date_to}.xlsx"'
    )

    with pd.ExcelWriter(response, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Summary", index=False)

        # Add domain breakdown sheet
        domain_data = {"Date": [], "Domain": [], "Active Time": [], "Idle Time": [], "Allowed": []}
        for report in reports:
            work_session = report.work_session
            activity_logs = ActivityLog.objects.filter(work_session=work_session)
            for log in activity_logs:
                domain_data["Date"].append(report.report_date.strftime("%Y-%m-%d"))
                domain_data["Domain"].append(log.domain_name)
                domain_data["Active Time"].append(format_seconds_to_time(log.active_seconds))
                domain_data["Idle Time"].append(format_seconds_to_time(log.idle_seconds))
                domain_data["Allowed"].append("Yes" if log.is_allowed else "No")

        if domain_data["Date"]:
            domain_df = pd.DataFrame(domain_data)
            domain_df.to_excel(writer, sheet_name="Domain Breakdown", index=False)

    return response


def export_date_range_summary_csv(date_from, date_to, employee_ids=None):
    """
    Export date range summary as CSV

    Args:
        date_from: Start date
        date_to: End date
        employee_ids: Optional list of employee IDs to filter

    Returns:
        HttpResponse with CSV file
    """
    reports = DailyEmployeeReport.objects.filter(
        report_date__gte=date_from, report_date__lte=date_to
    ).select_related("employee_id")

    if employee_ids:
        reports = reports.filter(employee_id__in=employee_ids)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="summary_report_{date_from}_{date_to}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Employee Name",
            "Date",
            "Total Work Time",
            "Productive Time",
            "Idle Time",
            "Violations",
            "Productivity %",
        ]
    )

    for report in reports:
        writer.writerow(
            [
                report.employee_id.get_full_name(),
                report.report_date.strftime("%Y-%m-%d"),
                format_seconds_to_time(report.total_work_time),
                format_seconds_to_time(report.productive_time),
                format_seconds_to_time(report.idle_time),
                report.violation_count,
                f"{report.get_productivity_percentage():.2f}%",
            ]
        )

    return response

