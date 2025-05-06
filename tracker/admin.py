from django.contrib import admin
from .models import Expense, Category, Budget, RecurringExpense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date', 'description')
    list_filter = ('category', 'date')
    search_fields = ('description',)
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_custom')
    list_filter = ('is_custom',)
    search_fields = ('name',)
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount_limit', 'start_date', 'end_date')
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(RecurringExpense)
class RecurringExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'frequency', 'due_date')
    list_filter = ('frequency',)
    readonly_fields = ('user', 'created_date')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)
