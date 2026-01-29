# Activity Monitoring Module

Employee Work Activity Monitoring Module for Horilla HRMS.

## Overview

This module tracks employee browser activity during work sessions (check-in to check-out) via a browser extension. It provides admin dashboards with charts, reports, and downloadable data.

## Features

- **Session-Bound Tracking**: Activity tracking only during check-in to check-out
- **Browser Extension Integration**: Mandatory browser extension for activity monitoring
- **Domain Policy Enforcement**: Configurable allowed domain lists per organization
- **Admin Dashboards**: Daily reports, employee-wise reports, charts, and analytics
- **Report Downloads**: CSV and Excel export functionality
- **Employee Profile Integration**: Activity tab in employee profiles (admin-only)

## Installation

1. The module is already registered in `INSTALLED_APPS` in `horilla/settings.py`
2. Run migrations:
   ```bash
   python manage.py makemigrations activity_monitoring
   python manage.py migrate
   ```
3. Install required Python packages (if not already installed):
   ```bash
   pip install plotly pandas xlsxwriter
   ```
4. Set up browser extension (see `browser_extension/README.md`)

## Models

- **WorkSession**: Tracks individual work sessions from check-in to check-out
- **ActivityLog**: Logs domain-based activity during sessions
- **ExtensionHeartbeat**: Tracks heartbeat pings from browser extension
- **AllowedDomain**: Maintains allowed domain lists per company
- **DailyEmployeeReport**: Denormalized summary table for fast reporting

## API Endpoints

All API endpoints are under `/api/activity-monitoring/`:

- `POST /api/activity-monitoring/session/token/` - Get session token (requires authentication)
- `POST /api/activity-monitoring/heartbeat/` - Send heartbeat ping
- `POST /api/activity-monitoring/activity-log/` - Log activity
- `GET /api/activity-monitoring/session/status/` - Get session status

## Permissions

- `activity_monitoring.view_worksession` - View reports (admin)
- `activity_monitoring.view_activitylog` - View detailed logs (admin)
- `activity_monitoring.add_alloweddomain` - Manage domains (admin)

## Usage

### For Admins

1. Navigate to **Activity Monitoring > Daily Reports** in the sidebar
2. Filter by date range and employee
3. View charts and download reports
4. Access individual employee reports from the table

### For Employees

- Employees check in/out normally via the attendance system
- Browser extension automatically starts/stops monitoring
- No employee self-access to monitoring data

### Managing Allowed Domains

1. Go to Django Admin
2. Navigate to **Activity Monitoring > Allowed Domains**
3. Add domains for each company (or leave company blank for global domains)

## Browser Extension

See `browser_extension/README.md` for installation and configuration instructions.

## Configuration

- **Token Expiry**: Default 12 hours (configurable in `activity_monitoring/api/views.py`)
- **Heartbeat Interval**: 30 seconds (configurable in `browser_extension/background.js`)
- **Idle Threshold**: 60 seconds (configurable in `browser_extension/content.js`)

## Notes

- Activity tracking only occurs during active work sessions
- No tracking of personal data, content, or keystrokes
- Domain names are extracted from URLs (not full URLs stored)
- Screenshot metadata support is optional and not implemented by default

## Troubleshooting

1. **Extension not connecting**: Check API base URL in extension settings
2. **No data in reports**: Ensure employees have checked in and extension is running
3. **Charts not displaying**: Ensure Plotly is installed (`pip install plotly`)
4. **Permission errors**: Ensure user has `activity_monitoring.view_worksession` permission

