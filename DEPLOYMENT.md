# Docker Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- Browser extension distributed separately to end users

## Quick Start

1. **Copy environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your production settings
   ```

2. **Build and start services:**
   ```bash
   docker-compose up -d --build
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f server
   ```

4. **Run management commands:**
   ```bash
   docker-compose exec server python3 manage.py <command>
   ```

## Activity Monitoring Module

The activity monitoring module is included in the Docker image. After deployment:

1. **Add allowed domains:**
   ```bash
   docker-compose exec server python3 manage.py add_test_domains
   ```

2. **Recalculate reports (if needed):**
   ```bash
   docker-compose exec server python3 manage.py recalculate_daily_reports
   ```

## Browser Extension

The browser extension is **NOT** included in the Docker image. It must be:
- Distributed separately to employees
- Installed in their browsers
- Configured to point to your production API URL

See `browser_extension/README.md` for installation instructions.

## Production Considerations

1. **Security:**
   - Change `SECRET_KEY` in `.env`
   - Set `DEBUG=False`
   - Configure proper `ALLOWED_HOSTS`
   - Use HTTPS and update `CSRF_TRUSTED_ORIGINS`

2. **Performance:**
   - Adjust Gunicorn workers based on server resources
   - Configure proper database connection pooling
   - Set up reverse proxy (nginx) for static files

3. **Backups:**
   - Regular database backups
   - Media files backup
   - Test restore procedures

4. **Monitoring:**
   - Set up logging aggregation
   - Monitor database performance
   - Track API endpoint health

## Troubleshooting

### Database Connection Issues
```bash
# Check database logs
docker-compose logs db

# Test database connection
docker-compose exec server python3 manage.py dbshell
```

### Migration Issues
```bash
# Reset migrations (CAUTION: Only in development)
docker-compose exec server python3 manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
# Recollect static files
docker-compose exec server python3 manage.py collectstatic --noinput
```

### Activity Monitoring Not Working
1. Verify browser extension is installed and configured
2. Check API endpoints are accessible
3. Verify allowed domains are configured:
   ```bash
   docker-compose exec server python3 manage.py shell
   >>> from activity_monitoring.models import AllowedDomain
   >>> AllowedDomain.objects.all()
   ```

## Health Checks

The Docker setup includes health checks:
- Server health check: Checks if Django is responding
- Database health check: Checks if PostgreSQL is ready

View health status:
```bash
docker-compose ps
```

