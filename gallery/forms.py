from django.forms import ModelForm
from gallery.models import Sculpture, Theme
from django import forms


# custom widget to hide default Django text
# for edit form image upload field
class NoTextClearableFileInput(forms.ClearableFileInput):
    template_name = 'gallery/widgets/custom_file_input.html'


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
            'image': NoTextClearableFileInput(attrs={
                    'class': 'form-control',
                }),
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
        }

    def __init__(self, *args, **kwargs):
        """
        Conditionally overrides the placeholder for the new_theme field
        depending on whether any themes exist
        """
        super().__init__(*args, **kwargs)
        self.fields['themes'].required = False
        if not Theme.objects.exists():
            self.fields['new_theme'].widget.attrs[
                'placeholder'] = 'Add your first theme (required)'
        else:
            self.fields['new_theme'].widget.attrs[
                'placeholder'] = 'or add a new theme'

    def clean(self):
        """
        Allows form validation with multiselect only, new_theme only,
        or both; rejects submission only if both are empty.
        """
        cleaned_data = super().clean()
        themes = cleaned_data.get('themes')
        new_theme = cleaned_data.get('new_theme', '').strip()
        if not (themes or new_theme):
            raise forms.ValidationError(
                'A sculpture must have at least one theme - select an '
                'existing one or add a new one.'
            )
        return cleaned_data


class ThemeForm(forms.ModelForm):
    """
    A form for editing theme records
    """
    class Meta:
        model = Theme
        fields = ['name', 'representative_sculpture']

    def __init__(self, *args, **kwargs):
        """
        Ensures that an edit theme form filters and displays
        only and all sculptures that have that particular theme
        """
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['representative_sculpture'].queryset = (
                self.instance.sculptures.all()
            )

    def clean_name(self):
        """
        Checks for name duplicates excluding editing and
        rewriting same name; strips whitespaces; raises
        validation errors
        """
        name = self.cleaned_data.get('name', '').strip()
        duplicate = Theme.objects.filter(name__iexact=name).exclude(
            pk=self.instance.pk).exists()
        if duplicate:
            raise forms.ValidationError(
                'A theme with this name already exists.')
        return name
