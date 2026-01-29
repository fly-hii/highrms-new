"""
Django management command to add test domains to allowed domains list

Usage:
    python manage.py add_test_domains

This command adds youtube.com and amazon.com (global) to the allowed domains
for testing purposes.
"""

from django.core.management.base import BaseCommand

from activity_monitoring.models import AllowedDomain


class Command(BaseCommand):
    help = "Add test domains (youtube.com and amazon.com) to allowed domains list"

    def handle(self, *args, **options):
        test_domains = ["youtube.com", "amazon.com"]

        created_count = 0
        skipped_count = 0

        for domain_name in test_domains:
            # Create global allowed domain (company_id=None)
            domain, created = AllowedDomain.objects.get_or_create(
                company_id=None,
                domain_name=domain_name,
                defaults={"is_active": True},
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully added domain: {domain_name} (global)'
                    )
                )
                created_count += 1
            else:
                # Domain already exists, ensure it's active
                if not domain.is_active:
                    domain.is_active = True
                    domain.save()
                    self.stdout.write(
                        self.style.WARNING(
                            f'Domain {domain_name} already existed but was inactive. Activated it.'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Domain {domain_name} already exists and is active. Skipped.'
                        )
                    )
                skipped_count += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Summary: {created_count} domains added, {skipped_count} already existed"
            )
        )

