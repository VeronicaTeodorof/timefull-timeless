from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import SculptureForm
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.
def gallery(request):
    return render(request, 'gallery/gallery.html')


@login_required
def add_sculpture(request):
    """
    Handle creation of a new sculpture.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == "POST":
        form = SculptureForm(request.POST, request.FILES)
        if form.is_valid():
            sculpture = form.save()
            messages.success(request, "Sculpture added.")
            return redirect('gallery:sculpture-detail', slug=sculpture.slug)
    else:
        form = SculptureForm()

    return render(request, 'gallery/add_sculpture.html', {'form': form})


def sculpture_detail(request, slug):
    """
    View for the sculpture detail page
    """
    return render(request, 'gallery/sculpture_detail.html')
