from django.contrib import admin

from task_manager.models import Task, SubTask, Category

admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Category)
