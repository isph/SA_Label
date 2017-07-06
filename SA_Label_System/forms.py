from django import forms

class signup_form(forms.Form):
    input_email = forms.CharField(label='input_email', max_length=100)
    input_username = forms.CharField(label='input_username', max_length=100)
    input_password = forms.CharField(label='input_password', max_length=100)
    confirm_password = forms.CharField(label='confirm_password', max_length=100)