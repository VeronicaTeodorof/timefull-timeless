from django.shortcuts import render

# Create your views here.
def order_history(request):
    return render(request, 'checkout/order_history.html')