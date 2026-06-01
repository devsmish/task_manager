from django.contrib import admin

from task_manager.models import Task, SubTask, Category


class TaskInline(admin.StackedInline):
    model = SubTask
    extra = 1
    max_num = 5


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskInline]
    list_display = ('show_title', 'description', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'categories', 'deadline', 'created_at')
    search_fields = ('title', 'description')

    @admin.display(description="Task title")
    def show_title(self, obj: Task) -> str:
        if len(obj.title) <= 10:
            return obj.title
        return f"{obj.title[:10]}..."


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'task', 'deadline', 'created_at')
    search_fields = ('title', 'description')
