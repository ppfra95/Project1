from django import forms
from django.contrib.auth import password_validation


__all__ = ['ChangePasswordForm', ]


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False
    )

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                'Las contraseñas no coinciden',
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password2', error)
