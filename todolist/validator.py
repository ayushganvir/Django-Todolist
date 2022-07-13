from django.forms import forms


def dash_validator(d):
    print(d)
    if d.find("-") >= 0:
        raise forms.ValidationError("Dash is not allowed")