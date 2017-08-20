from __future__ import absolute_import

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView

from core.models import Evento
from .forms import *


# Create your views here.


def registrar(request):

    if request.method == 'POST':
        form = CadastrarForm(request.POST)

        if form.is_valid():
            usuario = authenticate(username=form.cleaned_data['nomedeusuario'],
                                   password=form.cleaned_data['senha'])
            usuario = form.save()
            return redirect("base/login.html")
        else:
            return render(request, "base/cadastrar.html", {'form': form})
    else:
        form = CadastrarForm()
    return render(request, "base/cadastrar.html", {'form': form})

def home(request):
    return render(request, "base/home.html")

class CriarEvento(CreateView):
    model = Evento
    dono = Usuario
    template_name = 'base/evento_form.html'
    fields = ['titulo', 'descricao','tipo_evento', 'dt_inicio', 'dt_fim']

def editarEvento(request):
    #TODO
    return False

def removeEvento(request):
    #TODO
    return False

def addAtividade(request):
    #TODO
    return False

def removeAtividade(request):
    #TODO
    return False

def criarCupom(request):
    #TODO
    return False

@login_required
def alteraDados(request):
    #TODO
    return False

