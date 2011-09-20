from events.models import Invitee
from student.models import Student
for i in Invitee.objects.all():
    if not i.student:
        try:
            s = Student.objects.get(user__username=i.email)
            i.student = s
            i.save()
        except Student.DoesNotExist:
            pass