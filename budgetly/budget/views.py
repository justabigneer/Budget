from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from django import forms
from .models import Budget
from datetime import date

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ['monthly_income', 'savings_goal', 'month']
        widgets = {
            'month': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'monthly_income': forms.NumberInput(attrs={
                'step': '0.01', 
                'min': '0.01', 
                'class': 'form-control',
                'placeholder': '0.00'
            }),
            'savings_goal': forms.NumberInput(attrs={
                'step': '0.01', 
                'min': '0.00', 
                'class': 'form-control',
                'placeholder': '0.00'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default month to current month if not provided
        if not self.instance.pk:
            self.fields['month'].initial = date.today().replace(day=1)

@login_required
def setup(request):
    """Budget setup view"""
    current_month = date.today().replace(day=1)
    
    # Try to get existing budget for current month
    try:
        budget = Budget.objects.get(user=request.user, month=current_month)
    except Budget.DoesNotExist:
        budget = None
    
    if request.method == 'POST':
        if budget:
            form = BudgetForm(request.POST, instance=budget)
        else:
            form = BudgetForm(request.POST)
        
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            try:
                budget.save()
                messages.success(request, f'Budget saved successfully! Income: Nrs{budget.monthly_income}, Savings: Nrs{budget.savings_goal}')
                return redirect('reports:dashboard')
            except Exception as e:
                messages.error(request, f'Error saving budget: {str(e)}')
        else:
            # Add form errors to messages for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, f"Form error: {error}")
    else:
        if budget:
            form = BudgetForm(instance=budget)
        else:
            form = BudgetForm()
    
    return render(request, 'budget/setup.html', {'form': form, 'budget': budget})
