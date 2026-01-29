"""
urls.py

URL configuration for activity monitoring
"""

from django.urls import path

from activity_monitoring import views

app_name = "activity_monitoring"

urlpatterns = [
    path("daily-reports/", views.daily_reports_view, name="daily-reports"),
    path(
        "employee-report/<int:employee_id>/",
        views.employee_activity_report_view,
        name="employee-report",
    ),
    path(
        "employee-activity-tab/<int:emp_id>/",
        views.employee_activity_tab,
        name="employee-activity-tab",
    ),
    path("download/daily/", views.download_daily_report, name="download-daily"),
    path(
        "download/employee/<int:employee_id>/",
        views.download_employee_report,
        name="download-employee-report",
    ),
    path("download/summary/", views.download_summary_report, name="download-summary"),
]

