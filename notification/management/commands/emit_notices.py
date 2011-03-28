"""
 OpenSource
"""

import logging

from django.core.management.base import NoArgsCommand

from notification.engine import send_all

class Command(NoArgsCommand):
    help = "Emit queued notices."
    
    def handle_noargs(self, **options): #@UnusedVariable
        logging.basicConfig(level=logging.DEBUG, format="%(message)s") #@UnusedVariable
        logging.info("-" * 72)
        send_all()
    