from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class CadastrarForm(forms.ModelForm):
    senha = forms.CharField(label='senha', widget=forms.PasswordInput)

    def save(self, commit=True):
        usuario = super(CadastrarForm, self).save(commit=False)
        usuario.set_password(self.cleaned_data['senha'])
        usuario.save()

    class Meta:
        model = Usuario
        fields = ['nomedeusuario', 'email']
