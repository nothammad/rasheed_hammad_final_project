from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    BudgetListView, BudgetCreateView, BudgetUpdateView, BudgetDeleteView,
    RecurringExpenseListView, RecurringExpenseCreateView, RecurringExpenseUpdateView, RecurringExpenseDeleteView,
    dashboard_view,
    TransactionLogListView,
    SavingsGoalListView, SavingsGoalCreateView, SavingsGoalUpdateView, SavingsGoalDeleteView,
    NotificationListView, NotificationDeleteView,
    ProfileView, ProfileUpdateView, ProfileDeleteView,
    TagListView, TagCreateView, TagUpdateView, TagDeleteView,
    StaticAboutView, StaticHelpView, StaticFeedbackView,
)

urlpatterns = [
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    
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

    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),

    # Transaction Logs
    path('logs/', TransactionLogListView.as_view(), name='log-list'),

    # Savings Goals
    path('goals/', SavingsGoalListView.as_view(), name='goal-list'),
    path('goals/add/', SavingsGoalCreateView.as_view(), name='goal-create'),
    path('goals/<int:pk>/edit/', SavingsGoalUpdateView.as_view(), name='goal-update'),
    path('goals/<int:pk>/delete/', SavingsGoalDeleteView.as_view(), name='goal-delete'),

    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification-delete'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile-delete'),

    # Tags
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/add/', TagCreateView.as_view(), name='tag-create'),
    path('tags/<int:pk>/edit/', TagUpdateView.as_view(), name='tag-update'),
    path('tags/<int:pk>/delete/', TagDeleteView.as_view(), name='tag-delete'),

    # Static Pages 
    path('about/', StaticAboutView.as_view(), name='about'),
    path('help/', StaticHelpView.as_view(), name='help'),
    path('feedback/', StaticFeedbackView.as_view(), name='feedback'),
]
