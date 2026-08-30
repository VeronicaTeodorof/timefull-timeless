from django.forms import ModelForm
from gallery.models import Sculpture, Theme
from django import forms


class SculptureForm(ModelForm):
    """
    A form for adding and editing Sculpture records
    """
    new_theme = forms.CharField(
                required=False,
                label="Or type a new theme",
                widget=forms.TextInput(
                    attrs={'placeholder': 'or add a new theme',
                           'class': 'form-control'},
                                       )
            )

    class Meta:
        model = Sculpture
        fields = [
            'title',
            'title_translation',
            'dimensions',
            'year',
            'material',
            'price',
            'themes',
            'image',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Sculpture title (required)',
                       'class': 'form-control'}),
            'title_translation': forms.TextInput(
                attrs={'placeholder': 'Title translation (optional)',
                       'class': 'form-control'}),
            'dimensions': forms.TextInput(
                attrs={'placeholder': 'Dimensions (optional)',
                       'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'placeholder': 'Year (required)',
                                             'class': 'form-control'}),
            'material': forms.TextInput(
                attrs={'placeholder': 'Material (required)',
                       'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Price (required)',
                'class': 'form-control'}),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'themes': forms.CheckboxSelectMultiple(),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Conditionally overrides the placeholder for the new_theme field
        depending on whether any themes exist
        """
        super().__init__(*args, **kwargs)
        if not Theme.objects.exists():
            self.fields['new_theme'].widget.attrs[
                'placeholder'] = 'Add your first theme (required)'
        else:
            self.fields['new_theme'].widget.attrs[
                'placeholder'] = 'or add a new theme'

    # overriding the save method of the model form general pattern:
    # https://www.djangotricks.com/tricks/Swv44PDSrJYQ/
    # Django get_or_create() helper function:
    # https://docs.djangoproject.com/en/6.1/ref/models/querysets/#get-or-create
    # how to query case insensitive data in Django:
    # https://www.geeksforgeeks.org/python/how-to-query-case-insensitive-data-in-django-orm/
    def save(self, commit=True):
        sculpture = super().save(commit=commit)
        new_theme_name = self.cleaned_data.get('new_theme', '')
        if new_theme_name:
            theme = Theme.objects.filter(name__iexact=new_theme_name).first()
            if not theme:
                theme = Theme.objects.create(name=new_theme_name)
            sculpture.themes.add(theme)
        return sculpture
