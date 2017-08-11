from django import forms
from django.contrib.auth.models import User


class CadastrarForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='confirmar senha', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(CadastrarForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()

    class Meta:
        model = User
        fields = ['username', 'email']
