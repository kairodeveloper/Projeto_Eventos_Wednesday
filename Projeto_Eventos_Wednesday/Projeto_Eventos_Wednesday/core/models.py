from django.db import models
from enumfields import Enum, EnumField

# Create your models here.

#ENUM's
class TipoEvento(Enum):
    DEFAULT = 0
    SEMANA_CIENTIFICA = 1
    PALESTRA = 2
    CICLO_DE_PALESTRAS = 3
    SIMPOSIO = 4
    JORNADA = 5
    CONGRESSO = 6

class EstadoEvento(Enum):
    DEFAULT=0
    ABERTO = 1
    EM_ANDAMENTO = 2
    ENCERRADO = 3

class EstadoInscricao(Enum):
    NAO_PAGO=0
    PAGO = 1

class TipoApoio(Enum):
    APOIO = 0
    REALIZACAO = 1
    PATROCINIO = 2

class TipoAtividade(Enum):
    DEFAULT = 0
    PALESTRA = 1
    MINICURSO = 2
    MESAREDONDA = 3

#CLASSES MODELO
class Atividade(models.Model):
    cod_atividade = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=60)
    descricao = models.CharField(max_length=150)
    valor = models.FloatField()
    data = models.DateField()
    tipo_atividade = EnumField(TipoAtividade, default=TipoAtividade.DEFAULT)

class Usuario(models.Model):
    cod_user = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=9)
    email = models.CharField(max_length=45)
    senha = models.CharField(max_length=20)

class Evento(models.Model):
    cod_evento = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=45)
    descricao = models.CharField(max_length=200)
    administrador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_evento = EnumField(TipoEvento, default=TipoEvento.DEFAULT)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    estado_evento = EnumField(EstadoEvento, default=EstadoEvento.DEFAULT)
    atividades = models.ForeignKey(Atividade,on_delete=models.CASCADE)

class Cupom(models.Model):
    cod_cupom = models.IntegerField(primary_key=True)
    desconto = models.DecimalField()
    validade = models.DateField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

class Instituicao(models.Model):
    cod_instituicao = models.IntegerField(primary_key=True)
    endereco = models.CharField(max_length=60)
    descricao = models.CharField(max_length=200)

class Inscricao(models.Model):
    cod_inscricao = models.IntegerField(primary_key=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField()
    valor = models.FloatField()
    estado_inscricao = EnumField(EstadoInscricao, default=EstadoInscricao.NAO_PAGO)
    dia_pagamento = models.DateField()

class Apoio(models.Model):
    cod_apoio = models.IntegerField(primary_key=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    tipo_de_apoio = EnumField(TipoApoio, Default=TipoApoio.APOIO)