from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import date
from .forms import *
from usuario.models import *
import re

# Create your views here.

def page_criar_atividade(request, id_recebido):
    evento = Evento.objects.get(id=id_recebido)

    if request.method=='POST':
        form = CadastrarAtividadeForm(request.POST)
        data_inicio = recebe_data(request.POST.get('data_in'))
        valor = request.POST.get('valor')

        if form.is_valid():
            atividade = Atividade(titulo=form.cleaned_data['titulo'],
                                  descricao=form.cleaned_data['descricao'],
                                  tipo_atividade=form.cleaned_data['tipo_atividade'],
                                  data=data_inicio,
                                  valor=valor,
                                  evento=evento)
            atividade.save()


            cupons = Cupom.objects.filter(evento=evento)
            atividades = Atividade.objects.filter(evento=evento)
            apoios = ApoioEvento.objects.filter(evento=evento)

            return render(request, "base/evento_admin.html", {'evento': evento, 'atividades':atividades ,'cupons':cupons,'apoios':apoios})
        else:
            return render(request, "base/cadastrar_atividade.html", {'form': form})

    else:
        form = CadastrarAtividadeForm()
    return render(request, "base/cadastrar_atividade.html",{'form':form})

def page_evento(request, id_recebido):
    evento = Evento.objects.get(id=id_recebido)
    user = request.user

    cupons = Cupom.objects.filter(evento=evento)
    atividades = Atividade.objects.filter(evento=evento)
    apoios = ApoioEvento.objects.filter(evento=evento)

    valor_total = 0

    for i in atividades:
        valor_total+=float(i.valor)


    if request.method=='POST':
        data = date.today()

        pagamento = Pagamento(datapagamento=evento.dt_fim)
        pagamento.save()

        inscricao = Inscricao(evento=evento,
                              solicitante=request.user,
                              data_inscricao=data,
                              valor=str(valor_total),
                              pagamento=pagamento)
        inscricao.save()

        eventos = Evento.objects.all()
        eventos_non_user = []

        for i in eventos:
            if i.administrador.id != user.id:
                eventos_non_user.append(i)

        return render(request, "base/home.html", {'eventos': eventos_non_user})

    return render(request, "base/evento.html", {'evento': evento, 'atividades': atividades[::-1], 'cupons': cupons, 'apoios': apoios,'valor_total':valor_total})




def page_criar_cupom(request, id_recebido):
    evento = Evento.objects.get(id=id_recebido)

    if request.method == 'POST':
        data = recebe_data(request.POST.get('data_in'))
        desconto = float(request.POST.get('desconto'))/100

        cupom = Cupom(validade=data, desconto=desconto)
        cupom.cod_cupom = cupom._gerar_codigo_cupom()
        cupom.evento=evento
        cupom.save()

        cupons = Cupom.objects.filter(evento=evento)
        atividades = Atividade.objects.filter(evento=evento)
        apoios = ApoioEvento.objects.filter(evento=evento)

        return render(request, "base/evento_admin.html", {'evento': evento, 'atividades': atividades, 'cupons': cupons, 'apoios': apoios})

    return render(request, "base/novo_cupom.html")


def page_criar_apoios(request, id_recebido):

    evento = Evento.objects.get(id=id_recebido)

    if request.method == 'POST':
        form = CadastrarApoioForm(request.POST)
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        endereco = request.POST.get('endereco')

        if form.is_valid():
            instituicao = Instituicao(nome=nome,descricao=descricao,endereco=endereco)
            instituicao.save()
            apoio = ApoioEvento(evento=evento,
                                instituicao=instituicao,
                                tipo_apoio=form.cleaned_data['tipo_apoio'])
            apoio.save()

            cupons = Cupom.objects.filter(evento=evento)
            atividades = Atividade.objects.filter(evento=evento)
            apoios = ApoioEvento.objects.filter(evento=evento)

            return render(request, "base/evento_admin.html", {'evento': evento, 'atividades':atividades ,'cupons':cupons,'apoios':apoios})

    else:
        form = CadastrarApoioForm()
    return render(request, "base/novo_apoio.html",{"form":form})


def page_evento_admin(request, id_recebido):
    evento = Evento.objects.get(id=id_recebido)

    cupons = Cupom.objects.filter(evento=evento)
    atividades = Atividade.objects.filter(evento=evento)
    apoios = ApoioEvento.objects.filter(evento=evento)
    inscritos = Inscricao.objects.filter(evento=evento)

    return render(request, "base/evento_admin.html", {'evento': evento, 'atividades': atividades, 'cupons': cupons, 'apoios': apoios,'inscritos':inscritos})



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