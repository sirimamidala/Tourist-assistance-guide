import stripe
from django.conf import settings

class PaymentService:
    """
    Service helper for digital payment integration using Stripe.
    """
    @staticmethod
    def create_checkout_session(service_name, amount, success_url, cancel_url):
        stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)
        if not stripe.api_key:
            return {"error": "Stripe API Key missing. Payment is in mock mode."}

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': service_name,
                        },
                        'unit_amount': int(amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return {"url": session.url}
        except Exception as e:
            return {"error": str(e)}
