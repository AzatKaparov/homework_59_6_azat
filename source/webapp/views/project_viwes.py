from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from webapp.models import Project, Task
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from webapp.forms import SimpleSearchForm, ProjectForm, TaskForm, ProjectTaskForm


class ProjectIndexView(LoginRequiredMixin, ListView):
    template_name = 'project/index.html'
    context_object_name = 'projects'
    model = Project
    ordering = ['start_date']

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
            query = Q(name__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectView(LoginRequiredMixin, DetailView):
    template_name = 'project/project_view.html'
    model = Project


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_create.html'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectTaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'project/task_in_project_create.html'
    form_class = ProjectTaskForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)


class ProjectDeleteView(DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    success_url = reverse_lazy('webapp:project_index')


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project/project_update.html'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

