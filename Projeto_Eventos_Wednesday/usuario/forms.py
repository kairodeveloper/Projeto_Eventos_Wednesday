from django import forms
from .models import Usuario
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class CadastrarForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='confirmar senha', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(CadastrarForm, self).save(commit=False)
        user.set_password(self.cleaned_data['senha'])
        user.save()

    class Meta:
        model = Usuario
        fields = ['nome', 'email']
