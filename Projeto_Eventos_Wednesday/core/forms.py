from django import forms
from .models import *


class CadastrarForm(forms.ModelForm):
    login = forms.CharField(max_length=15, label='login')
    email = forms.EmailField(label='email')
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='confirmar senha', widget=forms.PasswordInput)
    #conf_password = forms.CharField( widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(CadastrarForm, self).save(commit=False)
        user.save()

    class Meta:
        model = Usuario
        fields = ['login', 'email', 'senha']
