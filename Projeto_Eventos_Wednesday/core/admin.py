from django.contrib import admin
from core.models import *
from django.contrib.auth.models import User

# Register your models here.

admin.site.register(Atividade)
admin.site.register(Evento)
admin.site.register(Cupom)
admin.site.register(Instituicao)
admin.site.register(Inscricao)
admin.site.register(Apoio)
