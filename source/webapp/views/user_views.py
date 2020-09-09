from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from webapp.models import Project, Task
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from webapp.forms import SimpleSearchForm, ProjectForm, TaskForm, ProjectTaskForm, UserAddForm


class AddUserProject(UpdateView):
    model = Project
    template_name = 'user/add_user.html'
    form_class = UserAddForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        form_kwargs = self.get_form_kwargs().get('data')
        form.save(commit=False)
        project.user.set(form_kwargs.get('user'))
        project.user.add(self.request.user)
        project.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)




