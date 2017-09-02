from django import forms
from .models import Usuario
from core.models import *
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


class CadastrarEventoForm(forms.ModelForm):

    class Meta:
        model = Evento
        fields = ['titulo','descricao','tipo_evento']


class CadastrarInstituicaoForm(forms.ModelForm):

    class Meta:
        model = Instituicao
        fields = ['endereco', 'descricao']