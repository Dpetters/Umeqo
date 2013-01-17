import stripe
import logging

from django.conf import settings as s
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from core.dict import Struct
from core.email import send_email
from subscription.view_helpers import get_or_create_receipt_pdf

sentry_logger = logging.getLogger("sentry.errors")

"""
Provides the following signals:

V1

- webhook_recurring_payment_failed
- webhook_invoice_ready
- webhook_recurring_payment_succeeded
- webhook_subscription_trial_ending
- webhook_subscription_final_payment_attempt_failed
- webhook_subscription_ping_sent

v2

- webhook_charge_succeeded
- webhook_charge_failed
- webhook_charge_refunded
- webhook_charge_disputed
- webhook_customer_created
- webhook_customer_updated
- webhook_customer_deleted
- webhook_customer_subscription_created
- webhook_customer_subscription_updated
- webhook_customer_subscription_deleted
- webhook_customer_subscription_trial_will_end
- webhook_customer_discount_created
- webhook_customer_discount_updated
- webhook_customer_discount_deleted
- webhook_invoice_created
- webhook_invoice_updated
- webhook_invoice_payment_succeeded
- webhook_invoice_payment_failed
- webhook_invoiceitem_created
- webhook_invoiceitem_updated
- webhook_invoiceitem_deleted
- webhook_plan_created
- webhook_plan_updated
- webhook_plan_deleted
- webhook_coupon_created
- webhook_coupon_updated
- webhook_coupon_deleted
- webhook_transfer_created
- webhook_transfer_failed
- webhook_ping
"""
import django.dispatch

WEBHOOK_ARGS = ["customer", "full_json"]

webhook_recurring_payment_failed = django.dispatch.Signal(providing_args=WEBHOOK_ARGS)
webhook_invoice_ready = django.dispatch.Signal(providing_args=WEBHOOK_ARGS)
webhook_recurring_payment_succeeded = django.dispatch.Signal(providing_args=WEBHOOK_ARGS)
webhook_subscription_trial_ending = django.dispatch.Signal(providing_args=WEBHOOK_ARGS)
webhook_subscription_final_payment_attempt_failed = django.dispatch.Signal(providing_args=WEBHOOK_ARGS)
webhook_subscription_ping_sent = django.dispatch.Signal(providing_args=[])

# v2 webhooks
WEBHOOK2_ARGS = ["full_json"]

webhook_charge_succeeded = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_charge_failed = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_charge_refunded = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_charge_disputed = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_created = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_updated = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_deleted = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_subscription_created = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_subscription_updated = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_subscription_deleted = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_subscription_trial_will_end = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_discount_created = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_discount_updated = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_customer_discount_deleted = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_invoice_created = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_invoice_updated = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_invoice_payment_succeeded = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_invoice_payment_failed = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_invoiceitem_created = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_invoiceitem_updated = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_invoiceitem_deleted = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_plan_created = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_plan_updated = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_plan_deleted = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_coupon_created = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_coupon_updated = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_coupon_deleted = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_transfer_created = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_transfer_failed = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)
webhook_ping = django.dispatch.Signal(providing_args=WEBHOOK2_ARGS)

WEBHOOK_MAP = {
    'charge_succeeded': webhook_charge_succeeded,
    'charge_failed': webhook_charge_failed,
    'charge_refunded': webhook_charge_refunded,
    'charge_disputed': webhook_charge_disputed,
    'customer_created': webhook_customer_created,
    'customer_updated': webhook_customer_updated,
    'customer_deleted': webhook_customer_deleted,
    'customer_subscription_created': webhook_customer_subscription_created,
    'customer_subscription_updated': webhook_customer_subscription_updated,
    'customer_subscription_deleted': webhook_customer_subscription_deleted,
    'customer_subscription_trial_will_end': webhook_customer_subscription_trial_will_end,
    'customer_discount_created': webhook_customer_discount_created,
    'customer_discount_updated': webhook_customer_discount_updated,
    'customer_discount_deleted': webhook_customer_discount_deleted,
    'invoice_created': webhook_invoice_created,
    'invoice_updated': webhook_invoice_updated,
    'invoice_payment_succeeded': webhook_invoice_payment_succeeded,
    'invoice_payment_failed': webhook_invoice_payment_failed,
    'invoiceitem_created': webhook_invoiceitem_created,
    'invoiceitem_updated': webhook_invoiceitem_updated,
    'invoiceitem_deleted': webhook_invoiceitem_deleted,
    'plan_created': webhook_plan_created,
    'plan_updated': webhook_plan_updated,
    'plan_deleted': webhook_plan_deleted,
    'coupon_created': webhook_coupon_created,
    'coupon_updated': webhook_coupon_updated,
    'coupon_deleted': webhook_coupon_deleted,
    'transfer_created': webhook_transfer_created,
    'transfer_failed': webhook_transfer_failed,
    'ping': webhook_ping,
}


def send_receipt(*args, **kwargs):
    stripe.api_key = s.STRIPE_SECRET
    
    # Get the invoice id
    charge = kwargs['full_json']['data']['object']
    charge = Struct(**charge)
    invoice = stripe.Invoice.retrieve(charge.invoice)
    
    try:
        customer = stripe.Customer.retrieve(charge.customer)
    except APIConnectionError as e:
        sentry_logger.warning("Customer %s paid for charge %s but did not get the receipt because the customer object could not be retrieved." % (charge.customer, charge.id))
    else:            
        employer_name = customer.description
        
        # We want to email all recruiters at the company
        users = User.objects.get(recruiter__employer__name=employer_name)
        recipients = map(lambda x: x.email, users)

        # Create receipt PDF attachment
        receipt_file_path = get_or_create_receipt_pdf(charge, invoice, employer_name)
        pdf_file = open(receipt_file_path, "rb")
        receipt_file_name = receipt_file_path.split("/")[-1]
        content = pdf_file.read()
        pdf_file.close()
        
        subject = ''.join(render_to_string('email_subject.txt', {
            'message': "Purchase Receipt"
        }, context).splitlines())
        
    send_email(subject, render_to_string("receipt_email_body.html", {}), recipients, receipt_file_name, content, "application/pdf")
    

webhook_charge_succeeded.connect(send_receipt)

