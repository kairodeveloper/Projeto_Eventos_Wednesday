from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import *
from .models import *
from core.models import *
from core.forms import *
from core.views import *
import re
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
            return render(request, "base/cadastrar_user.html", {'form': form})
    else:
        form = CadastrarForm()
    return render(request, "base/cadastrar_user.html", {'form': form})


@login_required()
def home(request):
    user = request.user
    eventos = Evento.objects.all()
    eventos_non_user = []

    for i in eventos:
        if i.administrador.id!=user.id:
            eventos_non_user.append(i)

    return render(request, "base/home.html", {'eventos':eventos_non_user})




@login_required
def criar_evento(request):
    administrador = request.user

    if request.method=='POST':
        form = CadastrarEventoForm(request.POST)
        data_inicio = recebe_data(request.POST.get('data_in'))
        data_fim = recebe_data(request.POST.get('data_out'))

        if form.is_valid():
            administrador.criar_evento(titulo=form.cleaned_data['titulo'],
                                       descricao=form.cleaned_data['descricao'],
                                       tipo_evento=form.cleaned_data['tipo_evento'],
                                       data_inicio=data_inicio,
                                       data_fim=data_fim)

            eventos = Evento.objects.all()
            evento = eventos[len(eventos)-1]
            return render(request,"base/evento_admin.html",{"evento":evento})
        else:
            return render(request, "base/cadastrar_evento.html", {'form': form})
    else:
       form = CadastrarEventoForm()

    return render(request, "base/cadastrar_evento.html",{'form': form})


def meus_eventos(request):
    usuario = request.user
    eventos = Evento.objects.filter(administrador=usuario)
    return render(request, "base/meus_eventos.html", {"usuario":usuario,"eventos":eventos})

#funcao: recebe o formato de data do materialize e converte para o formato do django
def recebe_data(sequencia):
    inicio = re.findall('(?P<Dia>[0]*[1-9]|[1-2][0-9]|[3][0-1])\s(?P<Mes>[A-Z][a-z]+),\s(?P<Ano>\d{4})', sequencia)
    meses_validos = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    dia = ""
    mes = ""
    ano = ""

    for i in range(len(meses_validos)-1):
        if (inicio[0][1] == meses_validos[i]):
            if (i >= 0 and i < 10):
                mes = "0" + str(i + 1)

            else:
                mes = str(i + 1)

    dia = inicio[0][0]
    ano = inicio[0][2]
    return ano + "-" + mes + "-" + dia

