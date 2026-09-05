from django.shortcuts import render
from gallery.models import Sculpture
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DeliveryCost
from pages.models import BusinessSettings


# Create your views here.
def order_history(request):
    return render(request, 'checkout/order_history.html')


@login_required
def terms_view(request, sculpture_slug):
    """
    A view for terms and conditions before proceeding to checkout
    """
    sculpture = get_object_or_404(Sculpture, slug=sculpture_slug)
    uk_cost = DeliveryCost.objects.get(country='UK')
    ro_cost = DeliveryCost.objects.get(country='RO')
    business_settings = BusinessSettings.load()
    insurance_cost = round(sculpture.price * business_settings.insurance_rate, 2)
    return render(request,
                  'checkout/terms.html',
                  {'sculpture': sculpture,
                   'uk_cost': uk_cost,
                   'ro_cost': ro_cost,
                   'insurance_cost': insurance_cost, })

