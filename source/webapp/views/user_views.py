from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from webapp.models import Project
from django.views.generic import UpdateView
from webapp.forms import UserAddForm


class AddUserProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'user/add_user.html'
    form_class = UserAddForm
    permission_denied_message = 'Отказано в доступе'
    permission_required = ('webapp.add_task',)
    # удаление юзера из списка чекбоксов по сути и есть удаление

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        form_kwargs = self.get_form_kwargs().get('data')
        form.save(commit=False)
        project.user.set(form_kwargs.get('user'))
        project.user.add(self.request.user)
        project.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)

    def has_permission(self):
        return Project.objects.filter(user=self.request.user, pk=self.get_object().pk) and super().has_permission()


