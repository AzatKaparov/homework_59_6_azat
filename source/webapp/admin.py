from django.contrib import admin
from .models import Type, Task, Status, Project


class TaskAdmin(admin.ModelAdmin):
    list_display = ('summary', 'status', 'created_at')
    fields = ['summary', 'description', 'status', 'type', 'project']
    search_fields = ('summary',)
    list_filter = ('status',)


admin.site.register(Task, TaskAdmin)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Project)