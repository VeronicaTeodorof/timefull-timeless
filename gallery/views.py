from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from gallery.models import Theme, Sculpture
from .forms import SculptureForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


# Create your views here.
def gallery(request):
    themes = Theme.objects.filter(sculptures__isnull=False).distinct()
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


@login_required
def edit_theme(request, slug):
    """
    View for the theme edit functionality
    """
    theme = get_object_or_404(Theme, slug=slug)
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == "POST":
        theme.name = request.POST.get('name')
        representative_sculpture_pk = request.POST.get(
            'representative_sculpture')
        # The modal's dropdown always has something pre-selected, so this
        # field is unlikely to arrive empty in practice - but some of this
        # project's own tests post only the name on purpose, to test renaming
        # in isolation, leaving this field genuinely absent.
        # Without the conditional check below,
        # get_object_or_404(Sculpture, pk=None) would raise Http404 and
        # stop theme.save() from ever running, even for an unrelated change.
        if representative_sculpture_pk:
            theme.representative_sculpture = get_object_or_404(
                Sculpture,
                pk=representative_sculpture_pk)
        theme.save()
        return HttpResponse("saved")
    return HttpResponse("ok")
