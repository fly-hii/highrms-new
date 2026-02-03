"""
App configuration for the 'payroll' app.
"""

from django.apps import AppConfig


class PayrollConfig(AppConfig):
    """
    AppConfig for the 'payroll' app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "payroll"

    def ready(self) -> None:
        super().ready()

        from django.urls import include, path
        from horilla.horilla_settings import APPS
        from horilla.urls import urlpatterns
        from payroll import signals  # noqa: F401

        # Register payroll app and URLs
        if "payroll" not in APPS:
            APPS.append("payroll")

        urlpatterns.append(
            path("payroll/", include("payroll.urls.urls")),
        )

        # Scheduler temporarily disabled due to DB startup issues
        # from payroll.scheduler import auto_payslip_generate
        # auto_payslip_generate()
