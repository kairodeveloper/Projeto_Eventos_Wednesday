from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _



class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nomedeusuario = models.CharField(max_length=30)
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Inscricao(models.Model):
    cod_inscricao = models.IntegerField(primary_key=True)
    evento = models.ForeignKey('core.Evento', on_delete=models.CASCADE)
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField()
    valor = models.FloatField()
    dia_pagamento = models.ForeignKey('core.Pagamento', on_delete=models.CASCADE)


class Item_Inscricao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    atividade = models.ForeignKey('core.Atividade', on_delete=models.CASCADE)
    horario = models.TimeField()
