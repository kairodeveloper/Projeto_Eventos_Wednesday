from django.db import models
from time import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


#class UsuarioManage(BaseUserManager):
#    def _create_user(self, email, senha,  is_staff, is_superuser, **extra_fields):

#        if not email:
#            raise ValueError('O email é obrigatorio')

#        email = self.normalize_email(email)
#        user = self.model(email=email,
#                          is_staff=is_staff,
#                          is_superuser=is_superuser,
#                          is_active=True, **extra_fields)

#        user.set_password(senha)
#        user.save(using=self._db)
#        return user

#    def create_user(self, email, password=None, **extra_fields):
#        return self._create_user(email, password, False, False, **extra_fields)

#    def create_superuser(self, email, password, **extra_fields):
#        return self._create_user(email, password, True, True, **extra_fields)


class Usuario(AbstractBaseUser):
    nomedeusuario = models.CharField(max_length=30)
    nome = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)

    USERNAME_FIELD = 'email'
    PASSWORD_FIELD = 'senha'
    REQUIRED_FIELDS = ['nome']

    #objects = UsuarioManage()

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
