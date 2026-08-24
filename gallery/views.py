from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import SculptureForm


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
    form = SculptureForm()
    return render(request, 'gallery/add_sculpture.html', {'form': form})
