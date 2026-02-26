from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'monthly_income', 'savings_goal', 'savings_percentage']
    list_filter = ['month', 'created_at']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'month'
    readonly_fields = ['created_at', 'updated_at']

    def savings_percentage(self, obj):
        return f"{obj.savings_percentage:.1f}%"
    savings_percentage.short_description = "Savings %"
