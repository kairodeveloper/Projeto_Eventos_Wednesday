from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from .forms import *

# Create your views here.


def registrar(request):

    if request.method == 'POST':
        form = CadastrarForm(request.POST)

        if form.is_valid():
            usuario = form.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "cadastrar.html", {'form': form})
    else:
        form = CadastrarForm()
    return render(request, "cadastrar.html", {'form': form})
