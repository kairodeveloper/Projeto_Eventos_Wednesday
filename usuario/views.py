from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import *
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
    eventos = Evento.objects.all()
    return render(request, "base/home.html", {'eventos':eventos})


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
            return render(request,"base/home.html", {'eventos': eventos,'msg':'Evento Criado'})

    else:
        apoios = [ ]
        form = CadastrarEventoForm()
        form2 = CadastrarInstituicaoForm()
        teste = ["kairo","kairo","kairo","kairo","kairo"]

    return render(request, "base/cadastrar_evento.html",{'form': form, 'form2':form2,'teste':teste})


def page_evento(request, id_recebido):
    evento = Evento.objects.get(id=id_recebido)
    return render(request, "base/evento.html", {'evento' : evento})


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

