from student.models import StudentPreferences, StudentStatistics

def create_student_related_models(sender, instance, created, raw, **kwargs):
    if created and not raw:
        if instance.first_name and instance.last_name:
            instance.user.first_name = instance.first_name
            instance.user.last_name = instance.last_name
            instance.user.save()
        StudentPreferences.objects.create(student=instance)
        StudentStatistics.objects.create(student=instance)