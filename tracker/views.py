from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Expense, Category, Budget, RecurringExpense
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json



# ---------- EXPENSE VIEWS ----------

def dashboard_view(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)
    budgets = Budget.objects.filter(user=user)

    total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_spent = round(float(total_spent),2)

    category_summary = (
        expenses.values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    chart_labels = [item['category__name'] or 'Uncategorized' for item in category_summary]
    chart_data = [round(float(item['total']),2) for item in category_summary]

    context = {
        'total_spent': round(total_spent,2),
        'category_summary': category_summary,
        'budgets': budgets,
        'chart_labels': mark_safe(json.dumps(chart_labels)),
        'chart_data': mark_safe(json.dumps(chart_data)),
    }
    return render(request, 'tracker/dashboard.html', context)

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'tracker/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        queryset = Expense.objects.filter(user=self.request.user)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name__icontains=category)
        return queryset.order_by('-date')


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    fields = ['category', 'amount', 'date', 'description']
    template_name = 'tracker/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['category', 'amount', 'date', 'description']
    template_name = 'tracker/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'tracker/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


# ---------- CATEGORY VIEWS ----------

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tracker/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'is_custom']
    template_name = 'tracker/category_form.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'is_custom']
    template_name = 'tracker/category_form.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'tracker/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


# ---------- BUDGET VIEWS ----------

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'tracker/budget_list.html'
    context_object_name = 'budgets'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    fields = ['category', 'amount_limit', 'start_date', 'end_date']
    template_name = 'tracker/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    fields = ['category', 'amount_limit', 'start_date', 'end_date']
    template_name = 'tracker/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'tracker/budget_confirm_delete.html'
    success_url = reverse_lazy('budget-list')

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


# ---------- RECURRING EXPENSE VIEWS ----------

class RecurringExpenseListView(LoginRequiredMixin, ListView):
    model = RecurringExpense
    template_name = 'tracker/recurring_list.html'
    context_object_name = 'recurring_expenses'

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)


class RecurringExpenseCreateView(LoginRequiredMixin, CreateView):
    model = RecurringExpense
    fields = ['category', 'amount', 'description', 'frequency', 'due_date']
    template_name = 'tracker/recurring_form.html'
    success_url = reverse_lazy('recurring-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RecurringExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = RecurringExpense
    fields = ['category', 'amount', 'description', 'frequency', 'due_date']
    template_name = 'tracker/recurring_form.html'
    success_url = reverse_lazy('recurring-list')

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)


class RecurringExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = RecurringExpense
    template_name = 'tracker/recurring_confirm_delete.html'
    success_url = reverse_lazy('recurring-list')

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)
