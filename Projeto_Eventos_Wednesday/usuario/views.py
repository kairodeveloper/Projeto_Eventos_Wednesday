from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import *
# Create your views here.


def registrar(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            usuario = authenticate(username=form.cleaned_data['username'],
                                   password=form.cleaned_data['password'])
            usuario = form.save()
            return redirect("/")
        else:
            return render(request, "base/cadastrar.html", {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, "base/cadastrar.html", {'form': form})


def home(request):
    return render(request, "base/home.html")
