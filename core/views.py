from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
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
            atividades = Atividade.objects.filter(evento=evento)
            return render(request, "base/evento_admin.html",{'evento':evento,'atividades':atividades})
        else:
            return render(request, "base/cadastrar_atividade.html", {'form': form})

    else:
        form = CadastrarAtividadeForm()
    return render(request, "base/cadastrar_atividade.html",{'form':form})

def page_evento(request, id_recebido):
    evento = Evento.objects.get(id=id_recebido)
    return render(request, "base/evento.html", {'evento' : evento})




def page_evento_admin(request, id_recebido):
    evento = Evento.objects.get(id=id_recebido)
    atividades = Atividade.objects.filter(evento=evento)
    return render(request, "base/evento_admin.html", {'evento' : evento, 'atividades' : atividades})




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