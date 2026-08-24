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
                widget=forms.TextInput(attrs={'placeholder': 'New theme name'})
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
