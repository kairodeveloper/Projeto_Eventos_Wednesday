from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings


class Usuario(AbstractBaseUser):
    nomedeusuario = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

    USERNAME_FIELD = 'nomedeusuario'
    REQUIRED_FIELDS = ['nome', 'senha', 'email']


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
