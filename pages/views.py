from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages


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
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request,
                             "Thank you - your message has been sent.")
            return redirect("pages:contact")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["email"] = request.user.email
        form = ContactForm(initial=initial)
    return render(request, "pages/contact.html", {"form": form})


def terms_view(request):
    return render(request, 'pages/terms.html')
