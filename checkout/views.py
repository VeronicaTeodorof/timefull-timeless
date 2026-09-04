from django.shortcuts import render
from gallery.models import Sculpture
from django.shortcuts import get_object_or_404


# Create your views here.
def order_history(request):
    return render(request, 'checkout/order_history.html')


def terms_view(request, sculpture_slug):
    """
    A view for terms and conditions before proceeding to checkout
    """
    sculpture = get_object_or_404(Sculpture, slug=sculpture_slug)
    return render(request,
                  'checkout/terms.html',
                  {'sculpture': sculpture})
