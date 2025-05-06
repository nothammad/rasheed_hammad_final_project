from django.contrib import admin
from .models import Expense, Category, Budget, RecurringExpense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('description',)

admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(RecurringExpense)
