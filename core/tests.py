from django.test import TestCase
import unittest
from core.models import *
from usuario.models import Usuario
from datetime import date
# Create your tests here.


#testar evento

class CoreTest(unittest.TestCase):

    def test_add_tag_com_nome(self):
        tamanho_antes = len(Tag.objects.all())

        nome = "Teste"

        tag=Tag(nome=nome)
        tag.save()

        tamanho_depois = len(Tag.objects.all())

        self.assertEquals(tamanho_depois,tamanho_antes+1)


    def test_add_local_com_todos_os_dados(self):
        tamanho_antes = len(Local.objects.all())


        nome="kairo"
        logradouro="uma rua ai"
        numero=40

        local = Local(nome=nome, logradouro=logradouro, numero=numero)
        local.save()

        tamanho_depois = len(Local.objects.all())

        self.assertEquals(tamanho_depois, tamanho_antes + 1)



    def test_add_evento(self):
        user = Usuario(nomedeusuario="User qualquer", email="emailqualquer", senha="senhaqualquer")
        user.save()
        local = Local(nome="nome", logradouro="logradouro", numero=40)
        local.save()

        tamanho_antes = len(Evento.objects.all())
        evento = Evento(titulo = "Teste Evento",
                        descricao = "Esse eh um teste basico de evento",
                        administrador = user,
                        dt_inicio = date.today(),
                        dt_fim = date.today(),
                        local = local,
                        valor = 50)

        evento.save()

        tamanho_depois = len(Evento.objects.all())

        self.assertEquals(tamanho_depois, tamanho_antes + 1)



    def test_add_instituicao(self):
        tamanho_antes = len(Instituicao.objects.all())

        instituicao = Instituicao(nome="InfoWay", endereco="endereco da IW",descricao="Empresa Topper")
        instituicao.save()

        tamanho_depois = len(Instituicao.objects.all())

        self.assertEquals(tamanho_depois, tamanho_antes + 1)



    def test_apoio_evento(self):
        tamanho_antes = len(ApoioEvento.objects.all())

        user = Usuario(nomedeusuario="User Qualquer", email="emailQualquer", senha="senhaqualquer")
        user.save()
        local = Local(nome="nome", logradouro="logradouro", numero=40)
        local.save()

        instituicao = Instituicao(nome="InfoWay", endereco="endereco da IW", descricao="Empresa Topper")
        instituicao.save()

        evento = Evento(titulo="Teste Evento",
                        descricao="Esse eh um teste basico de evento",
                        administrador=user,
                        dt_inicio=date.today(),
                        dt_fim=date.today(),
                        local=local,
                        valor=50)

        evento.save()

        apoio = ApoioEvento(evento=evento, instituicao=instituicao)
        apoio.save()

        tamanho_depois = len(ApoioEvento.objects.all())

        self.assertEquals(tamanho_depois, tamanho_antes + 1)


    def test_espaco_fisico(self):

        tamanho_antes = len(EspacoFisico.objects.all())


        espaco=EspacoFisico(nome="Espaco", lotacao=45).save()

        tamanho_depois = len(EspacoFisico.objects.all())

        self.assertEquals(tamanho_depois, tamanho_antes + 1)



    def test_responsavel(self):
        tamanho_antes = len(Responsavel.objects.all())

        resp = Responsavel(nome="Carinha", descricao="carinha que faz tudo").save()

        tamanho_depois = len(Responsavel.objects.all())

        self.assertEquals(tamanho_depois, tamanho_antes + 1)

