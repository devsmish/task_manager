import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

"""Выполните запросы:
1. Создание записей:
Task:
title: "Prepare presentation".
description: "Prepare materials and slides for the presentation".
status: "New".
deadline: Today's date + 3 days."""
from task_manager.models import Task, SubTask
from django.utils import timezone
from datetime import timedelta

main_task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status='new',
    deadline=timezone.now() + timedelta(days=3)
)

"""SubTasks для "Prepare presentation":
title: "Gather information".
description: "Find necessary information for the presentation".
status: "New".
deadline: Today's date + 2 days.
title: "Create slides".
description: "Create presentation slides".
status: "New".
deadline: Today's date + 1 day."""
subtasks = [
    SubTask(
        title="Gather information",
        description="Find necessary information for the presentation",
        status='new',
        deadline=timezone.now() + timedelta(days=1),
        task=main_task),
    SubTask(
        title="Create slides",
        description="Create presentation slides",
        status='new',
        deadline=timezone.now() + timedelta(days=1),
        task=main_task),
]

SubTask.objects.bulk_create(subtasks)

"""Чтение записей:
Tasks со статусом "New":
Вывести все задачи, у которых статус "New"."""
tasks = Task.objects.filter(status="new")
print(tasks)
print("------- TASK LIST -------")
for task in tasks:
    print(f"ID:{task.id} Title {task.title}")
    print(f"Deadline: {task.deadline}")
    print(f"Description: {task.description}")
    print(f"Creates at: {task.created_at}")
    print("-" * 25)

"""SubTasks с просроченным статусом "Done":
Вывести все подзадачи, у которых статус "Done", но срок выполнения истек."""
subtasks = SubTask.objects.filter(
    status='done',
    deadline__lt=timezone.now()
)

print(subtasks)

"""Изменение записей:
Измените статус "Prepare presentation" на "In progress"."""
task = Task.objects.filter(title="Prepare presentation").update(status='in_progress')

"""Измените срок выполнения для "Gather information" на два дня назад."""
subtask1 = SubTask.objects.filter(title="Gather information").update(deadline=timezone.now() - timedelta(days=2))

"""Измените описание для "Create slides" на "Create and format presentation slides"."""
subtask2 = SubTask.objects.filter(title="Create slides").update(description="Create and format presentation slides")

"""Удаление записей:
Удалите задачу "Prepare presentation" и все ее подзадачи."""
del_subtasks = SubTask.objects.filter(task__title="Prepare presentation").delete()
del_task = Task.objects.filter(title="Prepare presentation").delete()
