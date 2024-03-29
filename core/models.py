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
    OUTROS = 0
    PALESTRA = 1
    MINICURSO = 2
    MESAREDONDA = 3


class TipoInscricaoEvento(Enum):
    AUTOMATICO = 0
    MANUAL = 1


class TipoLazer(Enum):
    DEFAULT = 0
    COFFEBREAK = 1

class TipoResponsabilidade(Enum):
    PALESTRANTE = 0
    INSTRUTOR = 1
    MEDIADOR = 2

#CLASSES MODELO


class Tag(models.Model):
    nome = models.CharField(max_length=20,null=False, blank=False)


class Local(models.Model):
    nome = models.CharField(max_length=30)
    logradouro = models.CharField(max_length=30)
    numero = models.DecimalField("numero", max_digits=4, decimal_places=1)


class Evento(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=500)
    administrador = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, related_name='eventos_criados')
    tipo_evento = EnumField(TipoEvento, default=TipoEvento.OUTROS)
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    estado_evento = EnumField(EstadoEvento, default=EstadoEvento.ABERTO)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, default='')
    tipo_inscricao_evento = EnumField(TipoInscricaoEvento, default=TipoInscricaoEvento.MANUAL)
    valor = models.FloatField()
    evento_principal = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='eventos_satelites')

    def adicionar_atividade_incrita(self, titulo, local, trilha, responsavel, descricao, valor, data, tipo_atividade):
        atividade = Atividade(titulo=titulo, local=local, evento=self, responsavel=responsavel, descricao=descricao, valor=valor, data=data, tipo_atividade=tipo_atividade)
        atividade.save()

    def adicionar_atividade_lazer(self,atividade):
        atividade.evento = self
        atividade.save()

    def validar_data_evento(self, data_inicio, data_fim):
        if data_fim.date() < data_inicio.date():
            raise Exception("Data invalida ")

    def adicionar_a_equipe(self, usuario):
        funcionario = Funcionario(evento=self, usuario=usuario)
        funcionario.save()

    def equipe(self):
        return self.equipe

    def get_valor(self):
        return self.valor

    def apoio_realizacao(self):
        return self.apoio_evento

    def add_apoio_realizacao(self, instituicao, tipo_apoio):
        apoio = ApoioEvento(evento=self, instituicao=instituicao, tipo_apoio=tipo_apoio)
        apoio.save()

    def get_atividades(self):
        return self.atividades

    def adicionar_evento_satelite(self, evento):
        evento.evento_principal = self
        evento.save()




'''
class Sub_evento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE,
                               related_name='eventos_satelites', default='')
'''


class Instituicao(models.Model):
    nome = models.CharField(max_length=60)
    endereco = models.CharField(max_length=60)
    descricao = models.CharField(max_length=200)


class ApoioEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='apoio_evento')
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    tipo_apoio = EnumField(TipoApoio, default=TipoApoio.APOIO)

    def get_evento(self):
        return self.evento

    def get_instituicao(self):
        return self.instituicao


class EspacoFisico(models.Model):
    nome = models.CharField(max_length=30)
    lotacao = models.DecimalField("lotacao", max_digits=4, decimal_places=1)


class Responsavel(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.CharField(max_length=150)
    paginas = []
    tipo_responsabilidade = EnumField(TipoResponsabilidade, default=TipoResponsabilidade.MEDIADOR)


class Trilha(models.Model):
    tema = models.CharField(max_length=40)
    coordenador = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def atividades(self):
        return self.atividades

    def get_coordenador(self):
        return self.coordenador


class Atividade(models.Model):
    titulo = models.CharField(max_length=60)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class AtividadeInscrita(Atividade):
    responsavel = models.ForeignKey(Responsavel, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=150)
    valor = models.FloatField()
    data = models.DateField()
    horario = models.TimeField('horario', blank=True)
    tipo_atividade = EnumField(TipoAtividade, default=TipoAtividade.OUTROS)
    trilha = models.ForeignKey(Trilha, on_delete=models.CASCADE, related_name='atividades')
    espaco_fisico = models.ForeignKey(EspacoFisico, on_delete=models.CASCADE, related_name="atividade_inscrita")
    Atividade.evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='atividades_inscritas')

    def get_responsavel(self):
        return self.responsavel


class AtividadeLazer(Atividade):
    dt_inicio = models.DateField()
    dt_fim = models.DateField()
    tipo_lazer = EnumField(TipoLazer, default=TipoLazer.DEFAULT)
    Atividade.evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='atividades_lazer')

    def validar_data_atividade_lazer(self):
        if(dt_fim <= dt_inicio):
            raise Exception("Data final invalida")


class Cupom(models.Model):
    cod_cupom = models.CharField(primary_key=True, max_length=6)
    desconto = models.DecimalField("desconto", max_digits=3, decimal_places=2)
    validade = models.DateField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __init__(self):
        self.cod_cupom = self._gerar_codigo_cupom()

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
    gestor = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def realizar_pagamento(self, gestor, valor_pagamento):
        if valor_pagamento >= self.inscricao.valor:
            self.inscricao.status = self.inscricao.status.PAGO
            self.inscricao.save()
            self.datapagamento = date.today()
            self.gestor = gestor
            self.save()
        else:
            raise Exception("Pagamento nao efetuado")

