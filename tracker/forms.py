from django import forms
from .models import (
    Expense, Category, Budget, RecurringExpense, 
    TransactionLog, SavingsGoal, Notification, Profile, Tag
)
from .models import Profile
import pytz

# ----- EXPENSE FORM -----
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description','tags']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

# ----- CATEGORY FORM -----
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_custom']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ----- BUDGET FORM -----
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount_limit', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# ----- RECURRING EXPENSE FORM -----
class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = RecurringExpense
        fields = ['category', 'amount', 'description', 'frequency', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ----- SAVINGS GOAL FORM -----
class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['name', 'target_amount', 'deadline', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

# ----- PROFILE FORM -----
class ProfileForm(forms.ModelForm):
    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]

    timezone = forms.ChoiceField(choices=TIMEZONE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['timezone']

# ----- TAG FORM -----
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
