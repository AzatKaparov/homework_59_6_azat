from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.core.exceptions import ValidationError


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']
        field_classes = {'username': UsernameField}

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if not first_name:
            if not last_name:
                errors.append(ValidationError('Заполните хотя бы одно из двух полей!'))
        if not email:
            errors.append(ValidationError('Введите Email'))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


