from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from webapp.models import Task
from django.views.generic import TemplateView, FormView, ListView, DeleteView, UpdateView
from webapp.forms import TaskForm, SimpleSearchForm


class TaskIndexView(LoginRequiredMixin, ListView):
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    model = Task
    ordering = ['pk']
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class TaskView(LoginRequiredMixin, TemplateView):
    template_name = 'task/task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        context['task'] = task
        return context


class TaskCreateView(LoginRequiredMixin, FormView):
    template_name = 'task/task_create.html'
    form_class = TaskForm

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('webapp:view', kwargs={'pk': self.task.pk})

    def get_success_url(self):
        return reverse('webapp:view', kwargs={'pk': self.task.pk})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'task/task_delete.html'
    model = Task
    success_url = reverse_lazy('webapp:index')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'task/task_update.html'
    form_class = TaskForm
    model = Task

    def get_success_url(self):
        return reverse('webapp:view', kwargs={'pk': self.object.pk})
