from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json
from .models import Expense, Category, Budget, RecurringExpense, TransactionLog, SavingsGoal, Notification, Profile, Tag
from .forms import ProfileForm, ExpenseForm



# ---------- EXPENSE VIEWS ----------

@login_required
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
    form_class = ExpenseForm
    template_name = 'tracker/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        category = form.instance.category
        amount = form.instance.amount

        if category:
            budgets = Budget.objects.filter(user=self.request.user, category=category)
            for budget in budgets:
                spent = Expense.objects.filter(
                    user=self.request.user,
                    category=category,
                    date__range=[budget.start_date, budget.end_date]
                ).aggregate(total=Sum('amount'))['total'] or 0

                total_after = spent + amount
                if total_after > budget.amount_limit:
                    Notification.objects.create(
                        user=self.request.user,
                        message=f"You exceeded your budget for {category.name}. Limit: ${budget.amount_limit}, Spent: ${round(total_after, 2)}"
                    )
                    break
                  
        TransactionLog.objects.create(user=self.request.user, expense=self.object, action_type='created')
        return response


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    fields = ['category', 'amount', 'date', 'description']
    template_name = 'tracker/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        TransactionLog.objects.create(user=self.request.user, expense=self.object, action_type='updated')
        return response


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'tracker/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        TransactionLog.objects.create(user=self.request.user, expense=self.object, action_type='deleted')
        return super().delete(request, *args, **kwargs)


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

# ---------- SAVINGS GOAL VIEWS ----------
class SavingsGoalListView(LoginRequiredMixin, ListView):
    model = SavingsGoal
    template_name = 'tracker/savingsgoal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


class SavingsGoalCreateView(LoginRequiredMixin, CreateView):
    model = SavingsGoal
    fields = ['name', 'target_amount', 'deadline', 'notes']
    template_name = 'tracker/savingsgoal_form.html'
    success_url = reverse_lazy('goal-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SavingsGoalUpdateView(LoginRequiredMixin, UpdateView):
    model = SavingsGoal
    fields = ['name', 'target_amount', 'deadline', 'notes']
    template_name = 'tracker/savingsgoal_form.html'
    success_url = reverse_lazy('goal-list')

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


class SavingsGoalDeleteView(LoginRequiredMixin, DeleteView):
    model = SavingsGoal
    template_name = 'tracker/savingsgoal_confirm_delete.html'
    success_url = reverse_lazy('goal-list')

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)


# ---------- TRANSACTION LOG VIEWS ----------
class TransactionLogListView(LoginRequiredMixin, ListView):
    model = TransactionLog
    template_name = 'tracker/transactionlog_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return TransactionLog.objects.filter(user=self.request.user).order_by('-action_time')


# ---------- NOTIFICATION VIEWS ----------
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'tracker/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    template_name = 'tracker/notification_confirm_delete.html'
    success_url = reverse_lazy('notification-list')

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


# ---------- PROFILE VIEWS ----------
class ProfileView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'tracker/profile_view.html'
    context_object_name = 'profile'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'tracker/profile_form.html'
    success_url = reverse_lazy('profile-view')

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'tracker/profile_confirm_delete.html'
    success_url = reverse_lazy('profile-view')

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


# ---------- TAG VIEWS ----------
class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'tracker/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tracker/tag_form.html'
    success_url = reverse_lazy('tag-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    fields = ['name']
    template_name = 'tracker/tag_form.html'
    success_url = reverse_lazy('tag-list')

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'tracker/tag_confirm_delete.html'
    success_url = reverse_lazy('tag-list')

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


# ---------- STATIC PAGES ----------
class StaticAboutView(TemplateView):
    template_name = 'tracker/about.html'


class StaticHelpView(TemplateView):
    template_name = 'tracker/help.html'

class StaticFeedbackView(TemplateView):
    template_name = 'tracker/feedback.html'