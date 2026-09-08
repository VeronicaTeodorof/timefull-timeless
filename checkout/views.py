from gallery.models import Sculpture
from django.contrib.auth.decorators import login_required
from .models import DeliveryCost, Order, OrderLineItem
from pages.models import BusinessSettings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def order_history(request):
    return render(request, 'checkout/order_history.html')


@login_required
def terms_view(request, sculpture_slug):
    """
    A view for terms and conditions before proceeding to checkout
    """
    sculpture = get_object_or_404(Sculpture, slug=sculpture_slug)
    if sculpture.status == 'sold':
        messages.info(request, "This piece has already been acquired.")
        return redirect('gallery:sculpture-detail', sculpture_slug)
    uk_cost = DeliveryCost.objects.get(country='UK')
    ro_cost = DeliveryCost.objects.get(country='RO')
    business_settings = BusinessSettings.load()
    insurance_cost = round(
        sculpture.price * business_settings.insurance_rate, 2)
    return render(request,
                  'checkout/terms.html',
                  {'sculpture': sculpture,
                   'uk_cost': uk_cost,
                   'ro_cost': ro_cost,
                   'insurance_cost': insurance_cost, })


def create_checkout_session(request, sculpture_slug):
    """
    Creates a Stripe Checkout Session for the given sculpture, based
    on the buyer's shipping method (and country, if delivery) selected
    on the terms page, then redirects to Stripe's hosted checkout page.
    """
    sculpture = get_object_or_404(Sculpture, slug=sculpture_slug)
    if sculpture.status == 'sold':
        messages.info(request, "This piece has already been acquired.")
        return redirect('gallery:sculpture-detail', sculpture_slug)

    shipping_method = request.POST.get('shipping_method')
    country = request.POST.get('country')
    STRIPE_COUNTRY_CODES = {'UK': 'GB', 'RO': 'RO'}

    business_settings = BusinessSettings.load()
    insurance_cost = round(
        sculpture.price * business_settings.insurance_rate, 2)

    line_items = [
        {
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': sculpture.title,
                    'images': [sculpture.image.url],
                },
                'unit_amount': int(sculpture.price * 100),
            },
            'quantity': 1,
        },
        {
            'price_data': {
                'currency': 'gbp',
                'product_data': {'name': 'Insurance'},
                'unit_amount': int(insurance_cost * 100),
            },
            'quantity': 1,
        },
    ]
    session_params = {
        'payment_method_types': ['card'],
        'line_items': line_items,
        'mode': 'payment',
        'success_url': request.build_absolute_uri('/checkout/success/'),
        'cancel_url': request.build_absolute_uri(
            f'/checkout/terms/{sculpture_slug}/'
        ),
        'customer_email': request.user.email,
        'metadata': {
            'sculpture_slug': sculpture.slug,
            'shipping_method': shipping_method,
            'country': country or '',
            'user_id': str(request.user.id),
            'phone_number': request.POST.get('phone_number', ''),
        },
    }

    if shipping_method == 'delivery':
        delivery_cost = DeliveryCost.objects.get(country=country).cost
        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'product_data': {'name': f'Delivery ({country})'},
                'unit_amount': int(delivery_cost * 100),
            },
            'quantity': 1,
        })
        session_params['shipping_address_collection'] = {
            'allowed_countries': [STRIPE_COUNTRY_CODES[country]]
        }

    session = stripe.checkout.Session.create(**session_params)
    return redirect(session.url, code=303)


def checkout_success(request):
    """
    Bare success page for after Stripe redirects following a
    completed payment. Displays a simple confirmation for now.
    """
    return render(request, 'checkout/checkout_success.html')


# resources:
# - https://docs.stripe.com/webhooks/signature
# - Code Institute: 'Boutique Ado' project
# - inspecting real Checkout Session event payloads via the Stripe Dashboard
# - written with Claude AI assistance
@csrf_exempt
def payment_webhook(request):
    """
    Verifies incoming Stripe webhook events and processes confirmed
    checkout.session.completed events.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(content=str(e), status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object'].to_dict()
        metadata = session.get('metadata', {})

        user = User.objects.get(id=metadata.get('user_id'))
        sculpture = Sculpture.objects.get(slug=metadata.get('sculpture_slug'))

        customer_details = session.get('customer_details', {})
        shipping_details = session.get('collected_information',
                                       {}).get('shipping_details')

        full_name = customer_details.get('name')
        stripe_pid = session.get('payment_intent')
        phone_number = metadata.get('phone_number', '')

        if shipping_details:
            address = shipping_details.get('address', {})
            town_or_city = address.get('city')
            postcode = address.get('postal_code')
            street_address1 = address.get('line1')
            street_address2 = address.get('line2')
            country = address.get('country')
        else:
            town_or_city = street_address1 = postcode = street_address2 = None
            country = metadata.get('country', '')

        order = Order.objects.create(
            user=user,
            full_name=full_name,
            email=user.email,
            phone_number=phone_number,
            country=country,
            postcode=postcode,
            town_or_city=town_or_city,
            street_address1=street_address1,
            street_address2=street_address2,
            shipping_method=metadata.get('shipping_method'),
            stripe_pid=stripe_pid,
        )

        business_settings = BusinessSettings.load()
        insurance_cost = round(
            sculpture.price * business_settings.insurance_rate, 2)

        delivery_cost = 0
        if metadata.get('shipping_method') == 'delivery':
            delivery_cost = DeliveryCost.objects.get(
                country=metadata.get('country')).cost

        OrderLineItem.objects.create(
            order=order,
            sculpture=sculpture,
            price_at_purchase=sculpture.price,
            insurance_cost=insurance_cost,
            delivery_cost=delivery_cost,
        )

        # mark sculpture as sold after valid purchase
        sculpture.status = 'sold'
        sculpture.save()
        print("SCULPTURE STATUS SET TO:", sculpture.status)

        business_settings = BusinessSettings.load()
        # notify business owner when a new order is created
        send_mail(
            subject=f'New order: {sculpture.title}',
            message=(
                f"A new order has been placed.\n\n"
                f"Sculpture: {sculpture.title}\n"
                f"Buyer: {full_name} ({user.email})\n"
                f"Phone: {phone_number or 'Not provided'}\n"
                f"Shipping method: {metadata.get('shipping_method')}\n"
                f"Country: "
                f"{metadata.get('country') or '(Studio Pickup)'}\n"
                f"Order total: £{order.lineitems.first().lineitem_total}\n"
                f"Order number: {order.order_number}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[business_settings.owner_email],
        )

    return HttpResponse(status=200)
