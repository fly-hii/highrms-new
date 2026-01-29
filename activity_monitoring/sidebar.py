"""
sidebar.py

Sidebar configuration for activity monitoring
"""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

MENU = _("Activity Monitoring")
IMG_SRC = "images/ui/report.svg"
ACCESSIBILITY = "activity_monitoring.sidebar.menu_accessibility"

SUBMENUS = [
    {
        "menu": _("Daily Reports"),
        "redirect": reverse("activity_monitoring:daily-reports"),
        "accessibility": "activity_monitoring.sidebar.daily_reports_accessibility",
    },
]


def menu_accessibility(request, _menu: str = "", user_perms=None, *args, **kwargs) -> bool:
    """
    Check if user has permission to access activity monitoring menu
    Admin users (superuser or staff) have access by default
    """
    user = request.user
    if user.is_superuser or user.is_staff:
        return True
    return user.has_perm("activity_monitoring.view_worksession")


def daily_reports_accessibility(request, submenu, user_perms, *args, **kwargs) -> bool:
    """
    Check if user has permission to view daily reports
    Admin users (superuser or staff) have access by default
    """
    user = request.user
    if user.is_superuser or user.is_staff:
        return True
    return user.has_perm("activity_monitoring.view_worksession")

