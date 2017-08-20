import unittest
import core.models as core_models
from usuario.models import *
from django.db import models


class MyFuncTestCase(unittest.TestCase):
    pass
    #def testCriaEvento(self):
    #    usuario = Usuario(nomedeusuario="teste1",nome="kairoo", senha="123", email="sdnasdasdnan@gmail.com")
    #    usuario.save()

    #    self.assertEquals(usuario.criar_evento("tsfdt","vsdjavsdasf", core_models.TipoEvento.PALESTRA,"2017-12-12", "2017-12-12"), True)

    #    Usuario.objects.filter(nomedeusuario="kairo").delete()

    #def testListarEvento(self):
    #    usuario = Usuario(nomedeusuario="teste2",nome="nome", email="sdnasdnan@gmail.com", senha="123")
    #    usuario.save()

    #    usuario.criar_evento("tsfdt", "vsdjavsdasf", core_models.TipoEvento.PALESTRA, "2017-12-12", "2017-12-12")
    #    usuario.criar_evento("tsfdt", "vsdjavsdasf", core_models.TipoEvento.PALESTRA, "2017-12-12", "2017-12-12")
    #    usuario.criar_evento("tsfdt", "vsdjavsdasf", core_models.TipoEvento.PALESTRA, "2017-12-12", "2017-12-12")

    #    self.assertEquals(usuario.listar_evento(), 3)

    #    Usuario.objects.filter(nomedeusuario="kairo").delete()


    #def testInscreveEmEvento(self):
    #    usuario = Usuario(nomedeusuario="teste3",nome="kairoo", senha="123", email="asdnkjnasnfjan")
    #    usuario.save()
    #    evento = core_models.Evento("tsfdt", "vsdjavsdasf", core_models.TipoEvento.PALESTRA, "2017-12-12", "2017-12-12", administrador=usuario)

    #    usuario2 = Usuario(nomedeusuario="teste32", nome="nome", email="sdnassdnan@gmail.com", senha="123")

    #   self.assertEquals(usuario2.inscrever_evento(evento, "2017-08-20"), True)

    #    Usuario.objects.filter(nomedeusuario="teste3").delete()
    #    Usuario.objects.filter(nomedeusuario="teste32").delete()
