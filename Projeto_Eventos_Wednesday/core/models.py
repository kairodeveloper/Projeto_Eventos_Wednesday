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
    NAO_PAGO = 0
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
    administrador = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE)
    tipo_evento = EnumField(TipoEvento, default=TipoEvento.DEFAULT)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    estado_evento = EnumField(EstadoEvento, default=EstadoEvento.DEFAULT)
    atividades = models.ForeignKey(Atividade,on_delete=models.CASCADE)

    valor_evento = models.DecimalField()
    def __init___(self,titulo,cod_evento):
        self._titulo = titulo
        self._cod_evento = cod_evento

    def __str__(self):
        return self.titulo
    @property
    def titulo(self):
        print("Titulo do Evento: ")
        return self._titulo

    @property
    def atividades(self):
        return self.atividades.all()

    @property
    def administrador(self):
        return self.administrador
    def adicionar_atividade_evento(self,atividades):
        pass

    def validar_data_evento(self,data_inicio,data_fim):
        if data_fim.date() < data_inicio.date():
            raise Exception("Data invalida ")

class Cupom(models.Model):
    cod_cupom = models.IntegerField(primary_key=True)
    desconto = models.DecimalField("desconto", max_digits=3, decimal_places=2)
    validade = models.DateField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __init__(self,nome_cupom, desconto):
        self._desconto = desconto
        self._nome_cupom = nome_cupom

    @property
    def desconto(self):
        return self._desconto
    @desconto.setter
    def desconto(self,valor_desconto):
        if not  isinstance(int,float):
            raise ValueError("Valor de desconto invalido")
        self._desconto = valor_desconto
    def calcular_valor_cupom(self,valor_evento):
        return self._desconto * valor_evento

class Instituicao(models.Model):
    cod_instituicao = models.IntegerField(primary_key=True)
    endereco = models.CharField(max_length=60)
    descricao = models.CharField(max_length=200)


class Apoio(models.Model):
    cod_apoio = models.IntegerField(primary_key=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE,related_name='apoios')
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    tipo_de_apoio = EnumField(TipoApoio, default=TipoApoio.APOIO)


class Pagamento(models.Model):
    datapagamento = models.DateField()
    status = EnumField(EstadoInscricao, default=EstadoInscricao.NAO_PAGO)

class Inscricao(models.Model):
    cod_inscricao = models.IntegerField(primary_key=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField()
    valor = models.FloatField()
    estado_inscricao = EnumField(EstadoInscricao, default=EstadoInscricao.NAO_PAGO)
    dia_pagamento = models.DateField()

class Item_Inscricao(models.Model):
    cod_item = models.IntegerField(primary_key=True)
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    horario = models.TimeField()