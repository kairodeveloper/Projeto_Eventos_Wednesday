from django import forms
from .models import Usuario
from core.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CadastrarAtividadeForm(forms.ModelForm):

    class Meta:
        model = Atividade
        fields = ['titulo','descricao','tipo_atividade']

class CadastrarInstituicaoForm(forms.ModelForm):

    class Meta:
        model = Instituicao
        fields = ['endereco', 'descricao']

class CadastrarApoioForm(forms.ModelForm):

    class Meta:
        model = ApoioEvento
        fields = ['tipo_apoio']