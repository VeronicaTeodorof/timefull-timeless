from django.shortcuts import render
from .forms import ContactForm


# Create your views here.
def home(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    """
    Contact page view
    """
    form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})


def terms_view(request):
    return render(request, 'pages/terms.html')
