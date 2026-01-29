"""
charts.py

Chart generation functions using Plotly
"""

import json
from datetime import datetime, timedelta

import plotly.graph_objects as go
import plotly.express as px
from django.utils import timezone

from activity_monitoring.models import ActivityLog, DailyEmployeeReport, WorkSession
from employee.models import Employee


def generate_daily_productivity_chart(date, employee_id=None):
    """
    Generate daily productivity vs idle time bar chart

    Args:
        date: Date object
        employee_id: Optional employee ID to filter

    Returns:
        str: HTML div with chart
    """
    if employee_id:
        reports = DailyEmployeeReport.objects.filter(
            report_date=date, employee_id=employee_id
        )
    else:
        reports = DailyEmployeeReport.objects.filter(report_date=date)

    if not reports.exists():
        return "<div>No data available for this date</div>"

    employees = []
    productive_times = []
    idle_times = []

    for report in reports:
        employees.append(report.employee_id.get_full_name())
        productive_times.append(report.productive_time / 3600)  # Convert to hours
        idle_times.append(report.idle_time / 3600)

    fig = go.Figure(
        data=[
            go.Bar(name="Productive Time", x=employees, y=productive_times),
            go.Bar(name="Idle Time", x=employees, y=idle_times),
        ]
    )

    fig.update_layout(
        title="Daily Productivity vs Idle Time",
        xaxis_title="Employee",
        yaxis_title="Hours",
        barmode="group",
        height=400,
    )

    return fig.to_html(include_plotlyjs="cdn", div_id="daily-productivity-chart")


def generate_employee_comparison_chart(date_range, employee_ids):
    """
    Generate employee comparison stacked bar chart

    Args:
        date_range: Tuple of (start_date, end_date)
        employee_ids: List of employee IDs

    Returns:
        str: HTML div with chart
    """
    start_date, end_date = date_range
    reports = DailyEmployeeReport.objects.filter(
        report_date__gte=start_date,
        report_date__lte=end_date,
        employee_id__in=employee_ids,
    )

    if not reports.exists():
        return "<div>No data available for selected employees and date range</div>"

    # Aggregate data by employee
    employee_data = {}
    for report in reports:
        emp_name = report.employee_id.get_full_name()
        if emp_name not in employee_data:
            employee_data[emp_name] = {"productive": 0, "idle": 0}
        employee_data[emp_name]["productive"] += report.productive_time / 3600
        employee_data[emp_name]["idle"] += report.idle_time / 3600

    employees = list(employee_data.keys())
    productive = [employee_data[emp]["productive"] for emp in employees]
    idle = [employee_data[emp]["idle"] for emp in employees]

    fig = go.Figure(
        data=[
            go.Bar(name="Productive Time", x=employees, y=productive),
            go.Bar(name="Idle Time", x=employees, y=idle),
        ]
    )

    fig.update_layout(
        title="Employee Comparison (Productive vs Idle Time)",
        xaxis_title="Employee",
        yaxis_title="Hours",
        barmode="stack",
        height=400,
    )

    return fig.to_html(include_plotlyjs="cdn", div_id="employee-comparison-chart")


def generate_trend_chart(date_range, employee_id):
    """
    Generate trend analysis line chart

    Args:
        date_range: Tuple of (start_date, end_date)
        employee_id: Employee ID

    Returns:
        str: HTML div with chart
    """
    start_date, end_date = date_range
    reports = DailyEmployeeReport.objects.filter(
        report_date__gte=start_date,
        report_date__lte=end_date,
        employee_id=employee_id,
    ).order_by("report_date")

    if not reports.exists():
        return "<div>No data available for this employee and date range</div>"

    dates = [report.report_date.strftime("%Y-%m-%d") for report in reports]
    productive = [report.productive_time / 3600 for report in reports]
    idle = [report.idle_time / 3600 for report in reports]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=productive,
            mode="lines+markers",
            name="Productive Time",
            line=dict(color="green"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=idle,
            mode="lines+markers",
            name="Idle Time",
            line=dict(color="red"),
        )
    )

    fig.update_layout(
        title="Productivity Trend Over Time",
        xaxis_title="Date",
        yaxis_title="Hours",
        height=400,
    )

    return fig.to_html(include_plotlyjs="cdn", div_id="trend-chart")


def generate_domain_distribution_chart(date, employee_id=None):
    """
    Generate domain usage distribution pie chart

    Args:
        date: Date object
        employee_id: Optional employee ID to filter

    Returns:
        str: HTML div with chart
    """
    if employee_id:
        work_sessions = WorkSession.objects.filter(
            attendance_date=date, employee_id=employee_id, status="completed"
        )
    else:
        work_sessions = WorkSession.objects.filter(
            attendance_date=date, status="completed"
        )

    if not work_sessions.exists():
        return "<div>No data available for this date</div>"

    # Aggregate domain usage
    domain_usage = {}
    for session in work_sessions:
        activity_logs = ActivityLog.objects.filter(work_session=session)
        for log in activity_logs:
            if log.is_allowed:  # Only count allowed domains
                total_time = (log.active_seconds + log.idle_seconds) / 3600
                domain_usage[log.domain_name] = (
                    domain_usage.get(log.domain_name, 0) + total_time
                )

    if not domain_usage:
        return "<div>No domain data available</div>"

    # Get top 10 domains
    sorted_domains = sorted(domain_usage.items(), key=lambda x: x[1], reverse=True)[:10]
    domains = [d[0] for d in sorted_domains]
    times = [d[1] for d in sorted_domains]

    fig = go.Figure(data=[go.Pie(labels=domains, values=times, hole=0.3)])

    fig.update_layout(
        title="Top Domains Usage Distribution",
        height=400,
    )

    return fig.to_html(include_plotlyjs="cdn", div_id="domain-distribution-chart")

