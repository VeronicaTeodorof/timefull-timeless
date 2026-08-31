from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from gallery.models import Theme
from .forms import SculptureForm
from django.shortcuts import redirect
from django.contrib import messages


# Create your views here.
def gallery(request):
    themes = Theme.objects.all()
    return render(request, 'gallery/gallery.html', {'themes': themes})


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
            # saving the form of a m2m with 'commit=False'
            # https://docs.djangoproject.com/en/6.1/topics/forms/modelforms/
            sculpture = form.save(commit=False)
            sculpture.save()
            form.save_m2m()
            # retrieving lists from Query Dict
            # https://vonkunesnewton.medium.com/getting-lists-from-querydicts-django-bf648daead42
            new_theme_names = request.POST.getlist('new_theme')
            for name in new_theme_names:
                name = name.strip()
                if name:
                    theme = Theme.objects.filter(name__iexact=name).first()
                    if not theme:
                        theme = Theme.objects.create(name=name)
                    sculpture.themes.add(theme)
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
