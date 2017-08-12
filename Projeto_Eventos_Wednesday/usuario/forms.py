from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from django.contrib.auth import get_user_model

class CadastrarForm(UserCreationForm):

    def save(self, commit=True):
        user = super(CadastrarForm, self).save(commit=False)
        user.set_password(self.cleaned_data['senha'])
        user.save()

    class Meta:
        model = Usuario
        fields = ['nome', 'email']
