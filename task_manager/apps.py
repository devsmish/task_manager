from django.apps import AppConfig


class TaskManagerConfig(AppConfig):
    name = 'task_manager'

    def ready(self):
        import task_manager.signals # noqa: F401
