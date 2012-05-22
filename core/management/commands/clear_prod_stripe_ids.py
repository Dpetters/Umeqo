from django.core.management.base import BaseCommand

from employer.models import Employer

class Command(BaseCommand):
    help = "Clear all employer customer ids that got committed from prod."

    def handle(self, *args, **options):
        print options
        verbosity = int(options.get('verbosity', 1))
        print verbosity
        if verbosity > 1:
            print "Clearing prod employer stripe ids:"
        
        for employer in Employer.objects.all():
            if verbosity > 1:
                print "Processing %s" % employer
            employer.stripe_id = None
            employer.save();
        
        if verbosity > 1:
            print "Finished clearing prod employer stripe ids."
