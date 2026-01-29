"""
views.py

Views for activity monitoring dashboard and reports
"""

from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from activity_monitoring.filters import DailyEmployeeReportFilter
from activity_monitoring.methods.charts import (
    generate_daily_productivity_chart,
    generate_domain_distribution_chart,
    generate_employee_comparison_chart,
    generate_trend_chart,
)
from activity_monitoring.methods.reports import (
    export_date_range_summary_csv,
    export_daily_report_csv,
    export_employee_report_excel,
)
from activity_monitoring.methods.utils import format_seconds_to_time
from activity_monitoring.models import ActivityLog, DailyEmployeeReport, WorkSession
from employee.models import Employee
from horilla.decorators import hx_request_required, permission_required


@login_required
@permission_required("activity_monitoring.view_worksession")
def daily_reports_view(request):
    """
    Daily reports view - Admin dashboard for viewing daily activity reports
    """
    reports = DailyEmployeeReport.objects.all().select_related("employee_id").order_by(
        "-report_date", "employee_id"
    )

    # Apply filters
    filter_form = DailyEmployeeReportFilter(request.GET, queryset=reports)
    reports = filter_form.qs

    # Get filter values for template
    date_from = request.GET.get("report_date_from")
    date_to = request.GET.get("report_date_to")
    employee_id = request.GET.get("employee_id")

    # Generate charts if date is selected
    chart_html = None
    domain_chart_html = None
    if date_from and date_to:
        try:
            date_from_obj = date.fromisoformat(date_from)
            date_to_obj = date.fromisoformat(date_to)
            if employee_id:
                chart_html = generate_trend_chart(
                    (date_from_obj, date_to_obj), int(employee_id)
                )
            else:
                chart_html = generate_employee_comparison_chart(
                    (date_from_obj, date_to_obj),
                    list(reports.values_list("employee_id", flat=True).distinct()),
                )
        except Exception:
            pass

    if date_from:
        try:
            date_from_obj = date.fromisoformat(date_from)
            domain_chart_html = generate_domain_distribution_chart(
                date_from_obj, int(employee_id) if employee_id else None
            )
        except Exception:
            pass

    # Pagination
    paginator = Paginator(reports, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "reports": page_obj,
        "filter_form": filter_form,
        "chart_html": chart_html,
        "domain_chart_html": domain_chart_html,
        "date_from": date_from,
        "date_to": date_to,
        "employee_id": employee_id,
    }

    return render(request, "activity_monitoring/daily_reports.html", context)


@login_required
@permission_required("activity_monitoring.view_worksession")
def employee_activity_report_view(request, employee_id):
    """
    Individual employee activity report view
    """
    employee = get_object_or_404(Employee, id=employee_id)

    # Get date range from query params or default to last 30 days
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if not date_from:
        date_from = (date.today() - timedelta(days=30)).isoformat()
    if not date_to:
        date_to = date.today().isoformat()

    date_from_obj = date.fromisoformat(date_from)
    date_to_obj = date.fromisoformat(date_to)

    # Get reports
    reports = DailyEmployeeReport.objects.filter(
        employee_id=employee,
        report_date__gte=date_from_obj,
        report_date__lte=date_to_obj,
    ).order_by("-report_date")

    # Generate trend chart
    trend_chart_html = generate_trend_chart((date_from_obj, date_to_obj), employee_id)

    # Get activity logs for detailed view
    work_sessions = WorkSession.objects.filter(
        employee_id=employee,
        attendance_date__gte=date_from_obj,
        attendance_date__lte=date_to_obj,
        status="completed",
    )

    # Get domain breakdown
    domain_breakdown = {}
    for session in work_sessions:
        activity_logs = ActivityLog.objects.filter(work_session=session)
        for log in activity_logs:
            if log.domain_name not in domain_breakdown:
                domain_breakdown[log.domain_name] = {
                    "active": 0,
                    "idle": 0,
                    "allowed": log.is_allowed,
                }
            domain_breakdown[log.domain_name]["active"] += log.active_seconds
            domain_breakdown[log.domain_name]["idle"] += log.idle_seconds

    # Calculate summary statistics
    total_work_time = sum(r.total_work_time for r in reports)
    total_productive = sum(r.productive_time for r in reports)
    total_idle = sum(r.idle_time for r in reports)
    total_violations = sum(r.violation_count for r in reports)

    context = {
        "employee": employee,
        "reports": reports,
        "trend_chart_html": trend_chart_html,
        "domain_breakdown": domain_breakdown,
        "date_from": date_from,
        "date_to": date_to,
        "total_work_time": format_seconds_to_time(total_work_time),
        "total_productive": format_seconds_to_time(total_productive),
        "total_idle": format_seconds_to_time(total_idle),
        "total_violations": total_violations,
        "productivity_percentage": (
            (total_productive / total_work_time * 100) if total_work_time > 0 else 0
        ),
    }

    return render(request, "activity_monitoring/employee_report.html", context)


@login_required
@permission_required("activity_monitoring.view_worksession")
@hx_request_required
def employee_activity_tab(request, emp_id):
    """
    Employee activity tab view - For integration into employee profile
    Admin-only view showing activity monitoring data
    """
    employee = get_object_or_404(Employee, id=emp_id)

    # Get last 7 and 30 days summaries
    today = date.today()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)

    reports_7_days = DailyEmployeeReport.objects.filter(
        employee_id=employee, report_date__gte=last_7_days
    )
    reports_30_days = DailyEmployeeReport.objects.filter(
        employee_id=employee, report_date__gte=last_30_days
    )

    # Calculate summaries
    def calculate_summary(reports):
        total_work = sum(r.total_work_time for r in reports)
        total_productive = sum(r.productive_time for r in reports)
        total_idle = sum(r.idle_time for r in reports)
        total_violations = sum(r.violation_count for r in reports)
        return {
            "total_work_time": format_seconds_to_time(total_work),
            "total_productive": format_seconds_to_time(total_productive),
            "total_idle": format_seconds_to_time(total_idle),
            "total_violations": total_violations,
            "productivity_percentage": (
                (total_productive / total_work * 100) if total_work > 0 else 0
            ),
        }

    summary_7_days = calculate_summary(reports_7_days)
    summary_30_days = calculate_summary(reports_30_days)

    # Get recent violations
    recent_reports = DailyEmployeeReport.objects.filter(
        employee_id=employee, violation_count__gt=0
    ).order_by("-report_date")[:5]

    # Get top domains (last 30 days)
    work_sessions = WorkSession.objects.filter(
        employee_id=employee,
        attendance_date__gte=last_30_days,
        status="completed",
    )
    domain_usage = {}
    for session in work_sessions:
        activity_logs = ActivityLog.objects.filter(work_session=session, is_allowed=True)
        for log in activity_logs:
            domain_usage[log.domain_name] = (
                domain_usage.get(log.domain_name, 0)
                + log.active_seconds
                + log.idle_seconds
            )

    top_domains = sorted(domain_usage.items(), key=lambda x: x[1], reverse=True)[:10]

    context = {
        "employee": employee,
        "summary_7_days": summary_7_days,
        "summary_30_days": summary_30_days,
        "recent_reports": recent_reports,
        "top_domains": top_domains,
    }

    return render(request, "activity_monitoring/employee_activity_tab.html", context)


@login_required
@permission_required("activity_monitoring.view_worksession")
@require_http_methods(["GET"])
def download_daily_report(request):
    """
    Download daily report as CSV
    """
    report_date = request.GET.get("date")
    employee_id = request.GET.get("employee_id")

    if not report_date:
        return HttpResponse("Date parameter required", status=400)

    try:
        date_obj = date.fromisoformat(report_date)
    except ValueError:
        return HttpResponse("Invalid date format", status=400)

    if employee_id:
        try:
            employee_id = int(employee_id)
        except ValueError:
            return HttpResponse("Invalid employee ID", status=400)
    else:
        employee_id = None

    return export_daily_report_csv(date_obj, employee_id)


@login_required
@permission_required("activity_monitoring.view_worksession")
@require_http_methods(["GET"])
def download_employee_report(request, employee_id):
    """
    Download employee report as Excel
    """
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if not date_from or not date_to:
        return HttpResponse("date_from and date_to parameters required", status=400)

    try:
        date_from_obj = date.fromisoformat(date_from)
        date_to_obj = date.fromisoformat(date_to)
    except ValueError:
        return HttpResponse("Invalid date format", status=400)

    return export_employee_report_excel(employee_id, date_from_obj, date_to_obj)


@login_required
@permission_required("activity_monitoring.view_worksession")
@require_http_methods(["GET"])
def download_summary_report(request):
    """
    Download date range summary report as CSV
    """
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    employee_ids = request.GET.getlist("employee_ids")

    if not date_from or not date_to:
        return HttpResponse("date_from and date_to parameters required", status=400)

    try:
        date_from_obj = date.fromisoformat(date_from)
        date_to_obj = date.fromisoformat(date_to)
    except ValueError:
        return HttpResponse("Invalid date format", status=400)

    if employee_ids:
        try:
            employee_ids = [int(eid) for eid in employee_ids]
        except ValueError:
            return HttpResponse("Invalid employee IDs", status=400)
    else:
        employee_ids = None

    return export_date_range_summary_csv(date_from_obj, date_to_obj, employee_ids)
