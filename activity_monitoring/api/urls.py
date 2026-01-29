"""
api/urls.py

URL configuration for activity monitoring API
"""

from django.urls import path

from activity_monitoring.api.views import (
    ActivityLogView,
    BatchActivityLogView,
    HeartbeatView,
    SessionStatusView,
    SessionTokenView,
)

app_name = "activity_monitoring_api"

urlpatterns = [
    path("session/token/", SessionTokenView.as_view(), name="session-token"),
    path("heartbeat/", HeartbeatView.as_view(), name="heartbeat"),
    path("activity-log/", ActivityLogView.as_view(), name="activity-log"),
    path("activity-logs/batch/", BatchActivityLogView.as_view(), name="activity-logs-batch"),
    path("session/status/", SessionStatusView.as_view(), name="session-status"),
]

