from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Student, Attendance

@receiver(pre_delete, sender=Student)
def delete_attendance_records(sender, instance, **kwargs):
    Attendance.objects.filter(student=instance).delete()
