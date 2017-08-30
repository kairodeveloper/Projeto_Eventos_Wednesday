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

    if request.method == 'POST':

        titulo = request.POST.get('titulo_evento','titulo not found')
        descricao = request.POST.get('descricao_evento','descricao not found')
        tipo_recebido = request.POST.get('tipo', 'tipo not found')

        dia_inicio = request.POST.get('date_evento_in_day','dia in not found')
        mes_inicio = request.POST.get('date_evento_in_month','dia in not found')
        ano_inicio = request.POST.get('date_evento_in_year','dia in not found')
        inicio = str(ano_inicio)+"-"+str(mes_inicio)+"-"+str(dia_inicio)

        dia_fim = request.POST.get('date_evento_out_day','dia out not found')
        mes_fim = request.POST.get('date_evento_out_month','dia out not found')
        ano_fim = request.POST.get('date_evento_out_year','dia out not found')
        fim = str(ano_fim)+"-"+str(mes_fim)+"-"+str(dia_fim)


        tipo_evento = 0

        if(tipo_recebido==1):
            tipo_evento = TipoEvento.SEMANA_CIENTIFICA
        elif (tipo_recebido == 2):
            tipo_evento = TipoEvento.PALESTRA
        elif (tipo_recebido == 3):
            tipo_evento = TipoEvento.CICLO_DE_PALESTRAS
        elif (tipo_recebido == 4):
            tipo_evento = TipoEvento.SIMPOSIO
        elif (tipo_recebido == 5):
            tipo_evento = TipoEvento.JORNADA
        elif (tipo_recebido == 6):
            tipo_evento = TipoEvento.SEMANA_CIENTIFICA
        else:
            tipo_evento = TipoEvento.OUTROS

        administrador.criar_evento(titulo=titulo,descricao=descricao,tipo_evento=tipo_evento,data_inicio=inicio, data_fim=fim)
        eventos = Evento.objects.all()
        return render(request, "base/home.html", {'eventos':eventos})

    return render(request, "base/cadastrar_Evento.html")