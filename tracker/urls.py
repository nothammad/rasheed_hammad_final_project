from django.urls import path
from .views import (
    ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    BudgetListView, BudgetCreateView, BudgetUpdateView, BudgetDeleteView,
    RecurringExpenseListView, RecurringExpenseCreateView, RecurringExpenseUpdateView, RecurringExpenseDeleteView,
    dashboard_view,
)

urlpatterns = [
    # Expense URLs
    path('', ExpenseListView.as_view(), name='expense-list'),
    path('expenses/add/', ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # Budget URLs
    path('budgets/', BudgetListView.as_view(), name='budget-list'),
    path('budgets/add/', BudgetCreateView.as_view(), name='budget-create'),
    path('budgets/<int:pk>/edit/', BudgetUpdateView.as_view(), name='budget-update'),
    path('budgets/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget-delete'),

    # Recurring Expense URLs
    path('recurring/', RecurringExpenseListView.as_view(), name='recurring-list'),
    path('recurring/add/', RecurringExpenseCreateView.as_view(), name='recurring-create'),
    path('recurring/<int:pk>/edit/', RecurringExpenseUpdateView.as_view(), name='recurring-update'),
    path('recurring/<int:pk>/delete/', RecurringExpenseDeleteView.as_view(), name='recurring-delete'),

    path('dashboard/', dashboard_view, name='dashboard'),
]
