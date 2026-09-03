from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from gallery.models import Theme, Sculpture
from .forms import SculptureForm, ThemeForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
def gallery(request):
    themes = Theme.objects.filter(sculptures__isnull=False).distinct()
    return render(request, 'gallery/gallery.html', {'themes': themes})


@login_required
def add_sculpture(request):
    """
    Handles creation of a new sculpture.
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
    sculpture = get_object_or_404(Sculpture, slug=slug)
    return render(request,
                  'gallery/sculpture_detail.html',
                  {'sculpture': sculpture})


@login_required
def edit_theme(request, slug):
    """
    View for the theme edit functionality
    """
    theme = get_object_or_404(Theme, slug=slug)
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == "POST":
        form = ThemeForm(request.POST, instance=theme)
        if form.is_valid():
            form.save()
            messages.success(request, "Theme updated.")
            # resource for json response:
            # https://docs.djangoproject.com/en/6.1/ref/request-response/#jsonresponse-objects
            return JsonResponse({'success': True})
        return JsonResponse({'success': False,
                             'errors': form.errors.get(
                                 'name',
                                 ['Invalid submission.'])[0]}, status=400)
    return JsonResponse({'success': False,
                         'errors': 'Invalid request method.'}, status=400)


def edit_sculpture(request, slug):
    """
    Handles editing of a sculpture object
    """
    sculpture = get_object_or_404(Sculpture, slug=slug)
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == "POST":
        form = SculptureForm(request.POST, request.FILES, instance=sculpture)
        if form.is_valid():
            form.save()
            messages.success(request, "Sculpture updated.")
            return redirect('gallery:sculpture-detail', slug=sculpture.slug)
    else:
        form = SculptureForm(instance=sculpture)
    return render(request,
                  'gallery/edit_sculpture.html',
                  {'form': form, 'sculpture': sculpture})
