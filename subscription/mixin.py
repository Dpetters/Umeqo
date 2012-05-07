import stripe


def _get_attr_value(instance, attr, default=None):
    """
    Simple helper to get the value of an instance's attribute if it exists.

    If the instance attribute is callable it will be called and the result will
    be returned.

    Optionally accepts a default value to return if the attribute is missing.
    Defaults to `None`

    >>> class Foo(object):
    ...     bar = 'baz'
    ...     def hi(self):
    ...         return 'hi'
    >>> f = Foo()
    >>> _get_attr_value(f, 'bar')
    'baz'
    >>> _get_attr_value(f, 'xyz')

    >>> _get_attr_value(f, 'xyz', False)
    False
    >>> _get_attr_value(f, 'hi')
    'hi'
    """
    value = default
    if hasattr(instance, attr):
        value = getattr(instance, attr)
        if callable(value):
            value = value()
    return value


class StripeMixin(object):
    """
    Provides a property `stripe` that returns an instance of the Stripe module.

    It optionally supports the ability to set `stripe.api_key` if your class
    has a `stripe_api_key` attribute (method or property), or if
    settings has a `STRIPE_SECRET` attribute (method or property).
    """
    def _get_stripe(self):
        if hasattr(self, 'stripe_api_key'):
            stripe.api_key = _get_attr_value(self, 'stripe_api_key')
        elif hasattr(options, 'STRIPE_SECRET'):
            stripe.api_key = _get_attr_value(options, 'STRIPE_SECRET')
        return stripe
    stripe = property(_get_stripe)
    
class StripeCustomerMixin(object):
    """
    Provides a property property `stripe_customer` that returns a stripe
    customer instance.

    Your class must provide:
    
    - an attribute `stripe_customer_id` (method or property)
      to provide the customer id for the returned instance, and
    - an attribute `stripe` (method or property) that returns an instance
      of the Stripe module. StripeMixin is an easy way to get this.
    
    """
    def _get_stripe_customer(self):
        c = None
        if _get_attr_value(self, 'stripe_customer_id'):
            c = self.stripe.Customer.retrieve(_get_attr_value(self,
                                        'stripe_customer_id'))
        if not c and options.ZEBRA_AUTO_CREATE_STRIPE_CUSTOMERS:
            c = self.stripe.Customer.create()
            self.stripe_customer_id = c.id
            self.save()

        return c
    stripe_customer = property(_get_stripe_customer)