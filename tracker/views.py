from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Expense
from .forms import ExpenseForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "tracker/dashboard.html"

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = "tracker/expense_list.html"
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "tracker/expense_form.html"
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "tracker/expense_form.html"
    success_url = reverse_lazy('expense-list')

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = "tracker/expense_confirm_delete.html"
    success_url = reverse_lazy('expense-list')
