import stripe

from config.settings import STRIPE_API_KEY, DOMAIN_NAME

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name):
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(amount, product):
    price = stripe.Price.create(
        currency='rub',
        unit_amount=amount * 100,
        product_data={"name": product.get('name')},)
    return price


def create_stripe_session(price, instance_pk):
    session = stripe.checkout.Session.create(
        success_url=f'{DOMAIN_NAME}/payment/success/{instance_pk}',
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode='payment',)
    return session.get('id'), session.get('url')


def checkout_session(session_id):
    payment_status = stripe.checkout.Session.retrieve(session_id)
    return payment_status.get('payment_status')