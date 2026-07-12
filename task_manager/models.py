from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from task_manager.managers import SoftDeleteManager


class WeekDay(models.IntegerChoices):
    SUNDAY = 1, 'Sunday'
    MONDAY = 2, 'Monday'
    TUESDAY = 3, 'Tuesday'
    WEDNESDAY = 4, 'Wednesday'
    THURSDAY = 5, 'Thursday'
    FRIDAY = 6, 'Friday'
    SATURDAY = 7, 'Saturday'


statuses = [
    ('new', 'New'),
    ('in_progress', 'In progress'),
    ('pending', 'Pending'),
    ('blocked', 'Blocked'),
    ('done', 'Done'),
]

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class Category(SoftDeleteModel): # Наследуемся от нашего SoftDeleteModel
    '''Execution Category'''
    name = models.CharField(max_length=50)

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Owner')

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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Owner')

    def __str__(self):
        return self.title

    class Meta:
        db_table =  'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        unique_together = ['title']
