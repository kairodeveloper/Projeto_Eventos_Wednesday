from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import *

# Create your views here.


def cadastrar(request):

    if request.method == 'POST':
        form = CadastrarForm(request.POST)
        user = form.save()
    else:
        form = CadastrarForm()
    return render(request, "cadastrar.html", {'form': form})
