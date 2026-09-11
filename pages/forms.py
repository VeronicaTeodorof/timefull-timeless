from django import forms


class ContactForm(forms.Form):
    """
    A form for the contact page
    """
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    subject = forms.CharField(max_length=150, required=False)
    message = forms.CharField(widget=forms.Textarea)
