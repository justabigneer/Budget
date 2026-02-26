from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from django import forms
from django.db.models import Sum
from decimal import Decimal
from .models import Expense, Category
from budget.models import Budget

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

def check_budget_availability(user, expense_amount, expense_date):
    """
    Check if adding this expense would exceed the user's budget
    Returns tuple (is_valid, message, available_amount)
    """
    try:
        # Get budget for the expense month
        budget = Budget.objects.get(
            user=user, 
            month__year=expense_date.year,
            month__month=expense_date.month
        )
        
        # Calculate current month's total expenses
        current_expenses = Expense.objects.filter(
            user=user,
            date__year=expense_date.year,
            date__month=expense_date.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Calculate what total would be with this new expense
        new_total = current_expenses + Decimal(str(expense_amount))
        
        # Check against available budget
        available_budget = budget.available_budget
        
        if new_total > available_budget:
            remaining = available_budget - current_expenses
            return (False, 
                   f"This expense would exceed your monthly budget! "
                   f"Available: Nrs{remaining:.2f}, Trying to spend: Nrs{expense_amount:.2f}",
                   remaining)
        else:
            remaining = available_budget - new_total
            return (True, 
                   f"Expense within budget. Remaining after this expense: Nrs{remaining:.2f}",
                   remaining)
                   
    except Budget.DoesNotExist:
        return (False, 
               "No budget set for this month. Please create a budget first.",
               Decimal('0.00'))

@login_required
def expense_list(request):
    """List user's expenses"""
    expenses = Expense.objects.filter(user=request.user)[:20]
    return render(request, 'expenses/list.html', {'expenses': expenses})

@login_required
def add_expense(request):
    """Add new expense with budget validation"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense_amount = form.cleaned_data['amount']
            expense_date = form.cleaned_data['date']
            
            # Check budget availability
            is_valid, message, remaining = check_budget_availability(
                request.user, expense_amount, expense_date
            )
            
            if is_valid:
                expense = form.save(commit=False)
                expense.user = request.user
                expense.save()
                messages.success(request, f'Expense added successfully! {message}')
                return redirect('expenses:list')
            else:
                # Budget exceeded - show error and stay on form
                messages.error(request, message)
                # Re-populate form but don't save
    else:
        form = ExpenseForm()
    
    # Filter categories for the user
    form.fields['category'].queryset = Category.get_user_categories(request.user)
    
    # Add budget info to context for display
    context = {'form': form}
    try:
        from datetime import date
        current_budget = Budget.objects.get(
            user=request.user,
            month__year=date.today().year,
            month__month=date.today().month
        )
        
        # Calculate current month's expenses
        current_expenses = Expense.objects.filter(
            user=request.user,
            date__year=date.today().year,
            date__month=date.today().month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        context.update({
            'budget': current_budget,
            'current_expenses': current_expenses,
            'remaining_budget': current_budget.available_budget - current_expenses,
            'budget_percentage_used': (current_expenses / current_budget.available_budget * 100) if current_budget.available_budget > 0 else 0
        })
    except Budget.DoesNotExist:
        context['no_budget'] = True
    
    return render(request, 'expenses/add.html', context)
