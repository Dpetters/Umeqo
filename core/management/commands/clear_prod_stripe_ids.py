from django.core.management.base import BaseCommand

from employer.models import Employer

class Command(BaseCommand):
    help = "Clears all employer Stripe customer ids that got committed from prod."

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 1))
        if verbosity > 0:
            print "Clearing prod employer Stripe customer ids:"
        
        for employer in Employer.objects.all():
            if verbosity > 0:
                print "Processing %s" % employer
            employer.stripe_id = None
            employer.save();
        
        if verbosity > 0:
            print "Finished clearing prod employer Stripe customer ids."
