"""
Django management command to recalculate daily reports from activity logs

Usage:
    python manage.py recalculate_daily_reports [--employee-id ID] [--date YYYY-MM-DD]

This command recalculates daily reports from activity logs to fix any data inconsistencies.
"""

from django.core.management.base import BaseCommand

from activity_monitoring.methods.utils import generate_daily_report
from activity_monitoring.models import DailyEmployeeReport, WorkSession


class Command(BaseCommand):
    help = "Recalculate daily reports from activity logs to fix data inconsistencies"

    def add_arguments(self, parser):
        parser.add_argument(
            "--employee-id",
            type=int,
            help="Recalculate for specific employee ID only",
        )
        parser.add_argument(
            "--date",
            type=str,
            help="Recalculate for specific date (YYYY-MM-DD format)",
        )

    def handle(self, *args, **options):
        employee_id = options.get("employee_id")
        date_str = options.get("date")

        # Filter work sessions
        work_sessions = WorkSession.objects.filter(status="completed").select_related(
            "employee_id"
        )

        if employee_id:
            work_sessions = work_sessions.filter(employee_id=employee_id)
            self.stdout.write(f"Filtering for employee ID: {employee_id}")

        if date_str:
            from datetime import datetime

            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                work_sessions = work_sessions.filter(attendance_date=target_date)
                self.stdout.write(f"Filtering for date: {target_date}")
            except ValueError:
                self.stdout.write(
                    self.style.ERROR(f"Invalid date format: {date_str}. Use YYYY-MM-DD")
                )
                return

        total_sessions = work_sessions.count()
        self.stdout.write(f"Found {total_sessions} work sessions to recalculate...")
        self.stdout.write("")

        recalculated = 0
        for work_session in work_sessions:
            try:
                # Regenerate daily report
                generate_daily_report(work_session)
                recalculated += 1
                self.stdout.write(
                    f"Recalculated report for {work_session.employee_id.get_full_name()} "
                    f"on {work_session.attendance_date}"
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error recalculating for {work_session.employee_id.get_full_name()} "
                        f"on {work_session.attendance_date}: {str(e)}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Recalculation complete: {recalculated}/{total_sessions} reports updated"
            )
        )

