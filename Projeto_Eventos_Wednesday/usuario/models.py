from django.db import models
from time import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from enumfields import Enum, EnumField

from ..core.models import Evento


class EstadoInscricao(Enum):
    NAO_PAGO = 0
    PAGO = 1


class UsuarioManage(BaseUserManager):
    def _create_user(self, email, senha, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatorio')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(senha)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nomedeusuario = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def criar_evento(self,titulo,descricao,data_inicio,data_fim):
        evento = Evento(titulo=titulo,descricao=descricao,
                        data_inicio=data_inicio,data_fim=data_fim,
                        administrador=self)
        evento.save()

    USERNAME_FIELD = 'nomedeusuario'
    PASSWORD_FIELD = 'senha'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManage()

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def get_short_name(self):
        return self.nomedeusuario


class Inscricao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField()
    valor = models.DecimalField()
    dia_pagamento = models.ForeignKey('core.Pagamento', on_delete=models.CASCADE)
    atividades = models.ManyToManyField('core.Atividade', on_delete = models.CASCADE, related_name='atividades')
    status = EnumField(EstadoInscricao, default=EstadoInscricao.NAO_PAGO)

    def adicionar_atividade(self,atividade):
        if atividade in self.evento.atividades:
            self.atividades.add(atividade)
            self.valor += atividade.valor
        else:
            raise Exception("atividade nao adicionada")

    def aplicar_cupom(self,cupom):
        if cupom.validade_cupom():
            self.valor -= self.valor*cupom.desconto
        else:
            raise Exception("Cupom nao e valido  ")


class Item_Inscricao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE)
    atividade = models.ForeignKey('core.Atividade', on_delete=models.CASCADE)
    horario = models.TimeField()

