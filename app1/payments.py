import stripe

class PaymentService:
    def __init__(self):
        # Initialize the Stripe API client with your Stripe API key
        stripe.api_key = 'your_stripe_api_key'

    def process_payment(self, card_number, expiration_date, cvv):
        # Create a customer in Stripe
        customer = stripe.Customer.create()

        # Create a payment method using the provided card information
        payment_method = stripe.PaymentMethod.create(
            type='card',
            card={
                'number': card_number,
                'exp_month': expiration_date.month,
                'exp_year': expiration_date.year,
                'cvc': cvv
            }
        )

        # Attach the payment method to the customer
        stripe.PaymentMethod.attach(payment_method.id, customer=customer.id)

        # Make a payment using the attached payment method
        try:
            stripe.PaymentIntent.create(
                amount=1000,  # Amount in cents (e.g., $10.00)
                currency='usd',
                payment_method=payment_method.id,
                customer=customer.id,
                confirm=True
            )
        except stripe.error.CardError as e:
            # Handle card error
            return False
        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            return False

        # Payment succeeded
        return True