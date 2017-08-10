from django import forms
from .models import *


class CadastrarForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='confirmar senha', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(CadastrarForm, self).save(commit=False)
        user.save()

    class Meta:
        model = Usuario
        fields = ['login', 'email', 'senha']
