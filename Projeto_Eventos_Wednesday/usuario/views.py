from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
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

@login_required()
def home(request):
    return render(request, "base/home.html")

@login_required()
def criaEvento(request):
    #TODO
    return False

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

