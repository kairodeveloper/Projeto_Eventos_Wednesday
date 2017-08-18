from django.db import models
from time import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


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
    nome_usuario = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'nomedeusuario'
    PASSWORD_FIELD = 'senha'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManage()

    def __init__(self, nome, senha, email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nome = nome
        self.senha = senha
        self.email = email



    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def get_short_name(self):
        return self.nomedeusuario

class Inscricao(models.Model):
    cod_inscricao = models.IntegerField(primary_key =True)
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
