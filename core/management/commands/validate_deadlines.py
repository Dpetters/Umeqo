from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from events.models import Event, EventType

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for e in Event.objects.filter(type = EventType.objects.get(name="Hard Deadline")):
            e.start_datetime = e.end_datetime
            e.save()

        for e in Event.objects.filter(type = EventType.objects.get(name="Rolling Deadline")):
            e.start_datetime = datetime.now() - timedelta(weeks=1)
            e.save()