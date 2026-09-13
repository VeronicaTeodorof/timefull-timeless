from django import forms
from allauth.account.forms import LoginForm, SignupForm


class CustomLoginForm(LoginForm):
    """
    Custom login form for custom styling
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.widget.attrs.pop('placeholder', None)
            if field.required:
                field.label = f"{field.label} (required)"


class CustomSignupForm(SignupForm):
    """
    Custom sign up form for custom styling
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs.pop('placeholder', None)
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
