from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.shortcuts import render

from Projeto_Eventos_Wednesday.usuario.forms import *


# Create your views here.


def registrar(request):

    if request.method == 'POST':
        form = CadastrarForm(request.POST)

        if form.is_valid():
            usuario = authenticate(username=form.cleaned_data['username'],
                                   password=form.cleaned_data['password'])
            usuario = form.save()
            return redirect("/")
        else:
            return render(request, "cadastrar.html", {'form': form})
    else:
        form = CadastrarForm()
    return render(request, "cadastrar.html", {'form': form})


def home(request):
    return render(request, "home.html")
