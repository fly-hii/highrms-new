"""
utils.py

Utility functions for activity monitoring
"""

from collections import Counter
from datetime import datetime

from activity_monitoring.models import ActivityLog, AllowedDomain, DailyEmployeeReport
from base.models import Company


def normalize_domain(domain_name):
    """
    Normalize domain name for consistent comparison
    
    Args:
        domain_name: Domain name to normalize
        
    Returns:
        str: Normalized domain name (lowercase, without www.)
    """
    if not domain_name:
        return ""
    
    domain = domain_name.lower().strip()
    # Remove www. prefix
    if domain.startswith("www."):
        domain = domain[4:]
    
    return domain


def check_domain_allowed(domain_name, employee):
    """
    Check if a domain is allowed for the employee's company

    Args:
        domain_name: Domain name to check
        employee: Employee instance

    Returns:
        bool: True if domain is allowed, False otherwise
    """
    # Normalize domain name for consistent comparison
    normalized_domain = normalize_domain(domain_name)
    
    if not normalized_domain:
        return False
    
    try:
        company = employee.employee_work_info.company_id
    except Exception:
        company = None

    # Check company-specific allowed domains (normalized)
    if company:
        allowed_domains = AllowedDomain.objects.filter(
            company_id=company, is_active=True
        ).values_list("domain_name", flat=True)
        # Normalize all allowed domains for comparison
        normalized_allowed = [normalize_domain(d) for d in allowed_domains]
        if normalized_domain in normalized_allowed:
            return True

    # Check global allowed domains (company_id is None, normalized)
    global_allowed = AllowedDomain.objects.filter(
        company_id=None, is_active=True
    ).values_list("domain_name", flat=True)
    # Normalize all allowed domains for comparison
    normalized_global = [normalize_domain(d) for d in global_allowed]
    if normalized_domain in normalized_global:
        return True

    return False


def update_work_session_on_checkout(work_session):
    """
    Update work session statistics when employee checks out

    Args:
        work_session: WorkSession instance
    """
    # Aggregate activity logs for this session
    activity_logs = ActivityLog.objects.filter(work_session=work_session)

    total_active = sum(log.active_seconds for log in activity_logs)
    total_idle = sum(log.idle_seconds for log in activity_logs)

    work_session.total_active_seconds = total_active
    work_session.total_idle_seconds = total_idle
    work_session.save()


def generate_daily_report(work_session):
    """
    Generate or update daily employee report for a work session

    Args:
        work_session: WorkSession instance
    """
    # Get or create daily report
    daily_report, created = DailyEmployeeReport.objects.get_or_create(
        employee_id=work_session.employee_id,
        report_date=work_session.attendance_date,
        defaults={"work_session": work_session},
    )

    if not created:
        daily_report.work_session = work_session

    # Calculate statistics from activity logs
    activity_logs = ActivityLog.objects.filter(work_session=work_session)

    # Productive time: ONLY count active seconds from ALLOWED domains
    productive_time = sum(
        log.active_seconds 
        for log in activity_logs 
        if log.is_allowed is True
    )
    
    # Idle time: sum of all idle seconds (regardless of domain)
    idle_time = sum(log.idle_seconds for log in activity_logs)
    
    # Blocked active time: active time on blocked/not-allowed domains (non-productive)
    blocked_active_time = sum(
        log.active_seconds 
        for log in activity_logs 
        if log.is_allowed is False
    )
    
    # Total work time = productive time + idle time + blocked active time
    # This ensures totals always add up correctly
    total_work_time = productive_time + idle_time + blocked_active_time

    # Count violations (domains that are not allowed)
    violation_count = ActivityLog.objects.filter(
        work_session=work_session, is_allowed=False
    ).count()

    # Get top domains
    domain_counter = Counter()
    for log in activity_logs:
        domain_counter[log.domain_name] += log.active_seconds + log.idle_seconds

    top_domains = dict(domain_counter.most_common(10))

    # Update daily report
    daily_report.total_work_time = total_work_time
    daily_report.productive_time = productive_time
    daily_report.idle_time = idle_time
    daily_report.violation_count = violation_count
    daily_report.top_domains = top_domains
    daily_report.save()


def format_seconds_to_time(seconds):
    """
    Format seconds to HH:MM:SS format

    Args:
        seconds: Integer seconds

    Returns:
        str: Formatted time string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def extract_domain_from_url(url):
    """
    Extract domain name from a full URL

    Args:
        url: Full URL string

    Returns:
        str: Domain name
    """
    try:
        from urllib.parse import urlparse

        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split("/")[0]
        # Remove port if present
        domain = domain.split(":")[0]
        # Remove www. prefix
        if domain.startswith("www."):
            domain = domain[4:]
        return domain.lower()
    except Exception:
        # Fallback: try to extract domain manually
        if "://" in url:
            url = url.split("://")[1]
        if "/" in url:
            url = url.split("/")[0]
        if ":" in url:
            url = url.split(":")[0]
        if url.startswith("www."):
            url = url[4:]
        return url.lower()

