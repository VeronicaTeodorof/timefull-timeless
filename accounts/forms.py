from allauth.account.forms import LoginForm, SignupForm


class CustomLoginForm(LoginForm):
    """
    Custom login form for custom styling
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CustomSignupForm(SignupForm):
    """
    Custom sign up form for custom styling
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''
