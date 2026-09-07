from gallery.models import Sculpture
from django.contrib.auth.decorators import login_required
from .models import DeliveryCost
from pages.models import BusinessSettings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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
@csrf_exempt
def payment_webhook(request):
    """
    Bare version for testing signature verification only - confirms
    events from Stripe arrive correctly and are genuinely verified,
    before any business logic (Order creation, sold status, email)
    is added.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        # Any other unexpected error during verification
        return HttpResponse(content=str(e), status=400)

    print(f"Webhook received: {event['type']}")
    return HttpResponse(status=200)
