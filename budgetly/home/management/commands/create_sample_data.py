from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from budget.models import Budget
from expenses.models import Category, Expense
from datetime import date, timedelta
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Create sample data for testing the Budgetly application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='testuser',
            help='Username for the test user (default: testuser)'
        )
        parser.add_argument(
            '--password',
            type=str,
            default='testpass123',
            help='Password for the test user (default: testpass123)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='test@budgetly.com',
            help='Email for the test user (default: test@budgetly.com)'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        # Create or get the test user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created new user: {username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists')
            )

        # Create budget for current month
        current_month = date.today().replace(day=1)
        budget, created = Budget.objects.get_or_create(
            user=user,
            month=current_month,
            defaults={
                'monthly_income': Decimal('5000.00'),
                'savings_goal': Decimal('1000.00')
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created budget: Nrs{budget.monthly_income} income, Nrs{budget.savings_goal} savings goal')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Budget for current month already exists')
            )

        # Get all categories
        categories = Category.objects.filter(is_default=True)
        
        if not categories.exists():
            self.stdout.write(
                self.style.ERROR('No default categories found. Run "python manage.py create_default_categories" first.')
            )
            return

        # Sample expense data
        sample_expenses = [
            # Food & Dining
            ('Grocery Store', 'Food & Dining', Decimal('85.50')),
            ('Restaurant Dinner', 'Food & Dining', Decimal('45.00')),
            ('Coffee Shop', 'Food & Dining', Decimal('12.75')),
            ('Fast Food Lunch', 'Food & Dining', Decimal('18.99')),
            ('Pizza Delivery', 'Food & Dining', Decimal('32.50')),
            
            # Transportation
            ('Gas Station', 'Transportation', Decimal('55.00')),
            ('Uber Ride', 'Transportation', Decimal('18.50')),
            ('Parking Fee', 'Transportation', Decimal('15.00')),
            ('Bus Pass', 'Transportation', Decimal('85.00')),
            
            # Entertainment
            ('Movie Tickets', 'Entertainment', Decimal('28.00')),
            ('Streaming Service', 'Entertainment', Decimal('15.99')),
            ('Concert Tickets', 'Entertainment', Decimal('75.00')),
            ('Video Game', 'Entertainment', Decimal('59.99')),
            
            # Utilities
            ('Electric Bill', 'Utilities', Decimal('120.45')),
            ('Internet Bill', 'Utilities', Decimal('79.99')),
            ('Water Bill', 'Utilities', Decimal('45.50')),
            
            # Healthcare
            ('Pharmacy', 'Healthcare', Decimal('25.99')),
            ('Doctor Visit Copay', 'Healthcare', Decimal('35.00')),
            ('Gym Membership', 'Healthcare', Decimal('49.99')),
            
            # Shopping
            ('Clothing Store', 'Shopping', Decimal('89.99')),
            ('Online Purchase', 'Shopping', Decimal('45.50')),
            ('Bookstore', 'Shopping', Decimal('28.99')),
            
            # Housing
            ('Rent Payment', 'Housing', Decimal('1200.00')),
            ('Home Supplies', 'Housing', Decimal('65.75')),
            
            # Education
            ('Online Course', 'Education', Decimal('99.00')),
            ('Books', 'Education', Decimal('75.50')),
        ]

        # Create expenses for the past 30 days
        expenses_created = 0
        for i, (description, category_name, amount) in enumerate(sample_expenses):
            try:
                category = categories.get(name=category_name)
                
                # Create expenses spread over the last 30 days
                expense_date = date.today() - timedelta(days=random.randint(1, 30))
                
                expense, created = Expense.objects.get_or_create(
                    user=user,
                    description=description,
                    category=category,
                    amount=amount,
                    date=expense_date
                )
                
                if created:
                    expenses_created += 1
                    
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Category "{category_name}" not found, skipping expense "{description}"')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f'Created {expenses_created} sample expenses')
        )

        # Create a custom category for the user
        custom_category, created = Category.objects.get_or_create(
            user=user,
            name='Personal Projects',
            defaults={'is_default': False}
        )
        
        if created:
            # Add an expense for the custom category
            Expense.objects.create(
                user=user,
                category=custom_category,
                description='Website Development Tools',
                amount=Decimal('29.99'),
                date=date.today() - timedelta(days=5)
            )
            self.stdout.write(
                self.style.SUCCESS('Created custom category "Personal Projects" with sample expense')
            )

        # Summary
        total_expenses = Expense.objects.filter(user=user).count()
        total_spent = sum(expense.amount for expense in Expense.objects.filter(user=user))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n=== SAMPLE DATA CREATED SUCCESSFULLY ===\n'
                f'Test User: {username}\n'
                f'Password: {password}\n'
                f'Email: {email}\n'
                f'Monthly Income: Nrs{budget.monthly_income}\n'
                f'Savings Goal: Nrs{budget.savings_goal}\n'
                f'Total Expenses: {total_expenses}\n'
                f'Total Spent: Nrs{total_spent:.2f}\n'
                f'Remaining Budget: Nrs{budget.monthly_income - budget.savings_goal - total_spent:.2f}\n'
                f'\nYou can now login with username "{username}" and password "{password}"\n'
                f'to test all the features of Budgetly!'
            )
        )