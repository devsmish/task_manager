from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task


@receiver(pre_save, sender=Task)
def notify_owner_on_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    if old_instance.status != instance.status:
        if instance.owner and instance.owner.email:
            subject = f"Task '{instance.title}' status updated"

            old_status_display = old_instance.get_status_display()
            new_status_display = instance.get_status_display()

            message = (
                f"Hello, {instance.owner.username}!\n\n"
                f"The status of your task '{instance.title}' has been changed.\n"
                f"Old status: {old_status_display}\n"
                f"New status: {new_status_display}\n\n"
                f"Regards,\nTask Manager Bot"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[instance.owner.email],
                fail_silently=True,
            )