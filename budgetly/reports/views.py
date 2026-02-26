from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal
from expenses.models import Expense, Category
from budget.models import Budget
from datetime import date, timedelta
import json

@login_required
def dashboard(request):
    """Main dashboard with reports"""
    current_month = date.today().replace(day=1)
    
    # Get current budget
    try:
        budget = Budget.objects.get(user=request.user, month=current_month)
    except Budget.DoesNotExist:
        budget = None
    
    # Get this month's expenses
    expenses = Expense.objects.filter(
        user=request.user,
        date__month=current_month.month,
        date__year=current_month.year
    )
    
    # Calculate totals by category
    category_totals = expenses.values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Prepare chart data
    chart_labels = [item['category__name'] for item in category_totals]
    chart_data = [float(item['total']) for item in category_totals]
    # Convert chart_data values to Decimal and sum them
    total_spent = Decimal('0.00')
    for amount in chart_data:
        total_spent += Decimal(str(amount))
    
    # Savings goal analysis
    savings_analysis = None
    if budget:
        actual_savings = budget.monthly_income - total_spent
        target_savings = budget.savings_goal
        
        # Calculate savings goal achievement
        if target_savings > 0:
            savings_percentage = (actual_savings / target_savings) * Decimal('100')
            savings_met = actual_savings >= target_savings
            
            if savings_met:
                # Goal exceeded
                excess_amount = actual_savings - target_savings
                excess_percentage = (excess_amount / target_savings) * Decimal('100')
                savings_analysis = {
                    'goal_met': True,
                    'actual_savings': actual_savings,
                    'target_savings': target_savings,
                    'achievement_percentage': savings_percentage,
                    'excess_amount': excess_amount,
                    'excess_percentage': excess_percentage,
                    'status': 'exceeded' if excess_amount > 0 else 'met'
                }
            else:
                # Goal not met
                shortfall_amount = target_savings - actual_savings
                shortfall_percentage = (shortfall_amount / target_savings) * Decimal('100')
                savings_analysis = {
                    'goal_met': False,
                    'actual_savings': actual_savings,
                    'target_savings': target_savings,
                    'achievement_percentage': savings_percentage,
                    'shortfall_amount': shortfall_amount,
                    'shortfall_percentage': shortfall_percentage,
                    'status': 'missed'
                }
        else:
            # No savings goal set
            savings_analysis = {
                'goal_met': None,
                'actual_savings': actual_savings,
                'target_savings': target_savings,
                'status': 'no_goal'
            }
    
    context = {
        'budget': budget,
        'expenses': expenses[:10],  # Recent 10 expenses
        'total_spent': total_spent,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'savings_analysis': savings_analysis,
    }
    
    return render(request, 'reports/dashboard.html', context)
