from django.forms import ModelForm
from gallery.models import Sculpture
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
            'price': forms.NumberInput(attrs={'placeholder': 'Price (required)',
                                              'class': 'form-control'}),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'themes': forms.CheckboxSelectMultiple(),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
