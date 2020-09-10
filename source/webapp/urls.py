from django.urls import path
from webapp.views import TaskIndexView, TaskView, TaskDeleteView, TaskUpdateView, \
    ProjectIndexView, ProjectView, ProjectCreateView, ProjectTaskCreateView, ProjectDeleteView, \
    ProjectUpdateView, AddUserProject

app_name = 'webapp'

urlpatterns = [
    path('tasks', TaskIndexView.as_view(), name='index'),
    path('task/<int:pk>/', TaskView.as_view(), name='view'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('', ProjectIndexView.as_view(), name='project_index'),
    path('project/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('project/add', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/task/add/', ProjectTaskCreateView.as_view(), name='create_task_project'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/add_user/', AddUserProject.as_view(), name='add_user'),
]

