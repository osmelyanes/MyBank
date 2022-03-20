from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import exceptions
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from Account.models import Person


# Create your views here.
class CreateAccountForm(ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'iban']


class AccountListView(LoginRequiredMixin, ListView):
    model = Person
    paginate_by = 10
    template_name = "account_list.html"

    def get_queryset(self, **kwargs):
        user = self.request.user
        return Person.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Person
    template_name = "account_create_form.html"
    success_url = reverse_lazy('account-list')
    form_class = CreateAccountForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super(AccountCreateView, self).form_valid(form)


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Person
    fields = ['first_name', 'last_name', 'iban']
    template_name = "account_detail.html"
    success_url = reverse_lazy('account-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    template_name = "account_update_form.html"
    success_url = reverse_lazy('account-list')
    form_class = CreateAccountForm

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super(AccountUpdateView, self).form_valid(form)

    def get_object(self, queryset=None):
        qs = super(UpdateView, self).get_object(queryset)
        if qs.created_by == self.request.user:
            return qs
        else:
            raise exceptions.PermissionDenied("Cannot update other's accounts")


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Person
    template_name = "account_delete.html"
    success_url = reverse_lazy('account-list')

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by == request.user:
            instance.delete()
            return http.HttpResponseRedirect(self.success_url)
        else:
            raise PermissionDenied("Cannot delete other's accounts")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by == request.user:
            instance.delete()
            return http.HttpResponseRedirect(self.success_url)
        else:
            raise PermissionDenied("Cannot delete other's accounts")
