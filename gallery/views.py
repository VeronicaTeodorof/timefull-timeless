from django.shortcuts import render


# Create your views here.
def gallery(request):
    return render(request, 'gallery/gallery.html')


def add_sculpture(request):
    """
    Handle creation of a new sculpture.
    """
    return render(request, 'gallery/add_sculpture.html')
