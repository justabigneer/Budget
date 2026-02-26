from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Budget(models.Model):
    """Model for storing user's monthly budget information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    monthly_income = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    savings_goal = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    month = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'month']
        ordering = ['-month']

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}"

    @property
    def savings_percentage(self):
        """Calculate savings goal as percentage of income"""
        if self.monthly_income > 0:
            return (self.savings_goal / self.monthly_income) * 100
        return 0

    @property
    def available_budget(self):
        """Calculate available budget after savings"""
        return self.monthly_income - self.savings_goal
