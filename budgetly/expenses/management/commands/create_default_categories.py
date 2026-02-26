from django.core.management.base import BaseCommand
from expenses.models import Category

class Command(BaseCommand):
    help = 'Create default expense categories'

    def handle(self, *args, **options):
        default_categories = [
            'Food & Dining',
            'Transportation',
            'Entertainment',
            'Utilities',
            'Healthcare',
            'Shopping',
            'Housing',
            'Education',
        ]

        for category_name in default_categories:
            category, created = Category.objects.get_or_create(
                name=category_name,
                is_default=True
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created category "{category_name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category "{category_name}" already exists')
                )