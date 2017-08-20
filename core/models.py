from datetime import date
from string import ascii_uppercase, digits
import random
from django.db import models
from enumfields import Enum, EnumField
from usuario.models import *
# Create your models here.

#ENUM's


class TipoEvento(Enum):
    OUTROS = 0
    SEMANA_CIENTIFICA = 1
    PALESTRA = 2
    CICLO_DE_PALESTRAS = 3
    SIMPOSIO = 4
    JORNADA = 5
    CONGRESSO = 6


class EstadoEvento(Enum):
    ABERTO = 1
    EM_ANDAMENTO = 2
    ENCERRADO = 3


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


class Tag(models.Model):
    nome = models.CharField(max_length=20)
    #TODO tag many to many

class Evento(models.Model):
    titulo = models.CharField(max_length=45)
    descricao = models.CharField(max_length=200)
    administrador = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, related_name='eventos_criados')
    tipo_evento = EnumField(TipoEvento, default=TipoEvento.OUTROS)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    estado_evento = EnumField(EstadoEvento, default=EstadoEvento.ABERTO)

    def adicionar_atividade_evento(self,atividade):
        if atividade in self.atividades:
            raise Exception("ja esta cadastrado")
        else:
            self.atividades.append(atividade)

    def validar_data_evento(self,data_inicio,data_fim):
        if data_fim.date() < data_inicio.date():
            raise Exception("Data invalida ")

class Instituicao(models.Model):
    endereco = models.CharField(max_length=60)
    descricao = models.CharField(max_length=200)

class ApoioEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    tipo_apoio = EnumField(TipoApoio, default=TipoApoio.APOIO)


class Atividade(models.Model):
    titulo = models.CharField(max_length=60)
    descricao = models.CharField(max_length=150)
    valor = models.FloatField()
    data = models.DateField()
    tipo_atividade = EnumField(TipoAtividade, default=TipoAtividade.DEFAULT)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="atividades")


class Cupom(models.Model):
    cod_cupom = models.CharField(primary_key=True, max_length=6)
    desconto = models.DecimalField("desconto", max_digits=3, decimal_places=2)
    validade = models.DateField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def retornar_desconto(self):
        return self._desconto

    def mudar_valor_desconto(self,valor_desconto):
        if not isinstance(int, float):
            raise ValueError("Valor de desconto invalido")
        self._desconto = valor_desconto

    def validade_cupom(self):
        if date.today() <= self.validade:
            return True
        return False

    def _gerar_codigo_cupom(self):
        #gerar cupom randomically
        letras = list(ascii_uppercase)
        numeros = list(digits)
        letras_escolhida = random.sample(letras, 3)
        numeros_escolhidos = random.sample(numeros, 2)

        valor_gerado = letras_escolhida + numeros_escolhidos
        random.shuffle(valor_gerado)

        return "".join(valor_gerado)

    def calcular_valor_cupom(self,inscricao):
        return "%.2f ", (self._desconto * inscricao.valor)


class Pagamento(models.Model):
    datapagamento = models.DateField()

    def realizar_pagamento(self, valor_pagamento):
        if valor_pagamento >= self.inscricao.valor:
            self.inscricao.status = self.inscricao.status.PAGO
            self.inscricao.save()
            self.datapagamento = date.today()
            self.save()
        else:
            raise Exception("Pagamento nao efetuado")

