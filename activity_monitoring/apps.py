"""
apps.py
"""

from django.apps import AppConfig


class ActivityMonitoringConfig(AppConfig):
    """
    ActivityMonitoringConfig
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "activity_monitoring"
    verbose_name = "Activity Monitoring"

    def ready(self):
        """
        Import signals when app is ready
        """
        import activity_monitoring.signals  # noqa

