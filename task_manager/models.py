from django.db import models


statuses = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]

class Category(models.Model):
    '''Execution Category'''
    name = models.CharField(max_length=50) # Название категории. убрал unique=True

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ['name']


class Task(models.Model):
    '''Task to be completed'''
    title = models.CharField(max_length=250) # убрал unique_for_date='created_at'
    description = models.TextField(blank=True, default='') # Описание задачи.
    categories = models.ManyToManyField(Category) # Категории задачи.Многие ко многим.
    # Статус задачи.Выбор из: New, In progress, Pending, Blocked, Done
    status = models.CharField(max_length=25, choices=statuses, default='new')
    deadline = models.DateTimeField(null=True, blank=True) # Дата и время дедлайн.
    created_at = models.DateTimeField(auto_now_add=True) # Дата и время создания. Автоматическое заполнение.

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        unique_together = ['title']


class SubTask(models.Model):
    '''Individual Parts of the Main Task'''
    title = models.CharField(max_length=250) # Название подзадачи.
    description = models.TextField(blank=True, default='') # Описание подзадачи.
    task = models.ForeignKey(Task, on_delete=models.PROTECT) # Основная задача. Один ко многим.
    # Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
    status = models.CharField(max_length=25, choices=statuses, default='new')
    deadline = models.DateTimeField(null=True, blank=True) # Дата и время дедлайн.
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания. Автоматическое заполнение

    def __str__(self):
        return self.title

    class Meta:
        db_table =  'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        unique_together = ['title']
