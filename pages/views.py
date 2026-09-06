from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'pages/index.html')


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')


def terms_view(request):
    return render(request, 'pages/terms.html')
