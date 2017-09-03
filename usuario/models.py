from django.db import models
from time import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumField
from core import models as core_models


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

    def criar_evento(self, titulo, descricao, tipo_evento, data_inicio, data_fim):
        evento = core_models.Evento(titulo=titulo, descricao=descricao, tipo_evento=tipo_evento, dt_inicio=data_inicio, dt_fim=data_fim, administrador=self)
        evento.save()

    def listar_evento(self):
        return self.eventos_criados.all()

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
    evento = models.ForeignKey('core.Evento', on_delete=models.CASCADE, related_name='inscricoes')
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField()
    valor = models.DecimalField(max_digits=4, decimal_places=2)
    status = EnumField(EstadoInscricao, default=EstadoInscricao.NAO_PAGO)
    pagamento = models.ForeignKey('core.Pagamento', on_delete=models.CASCADE, related_name="inscricao")

    def adicionar_atividade(self, atividade):
        if atividade in self.evento.atividades:
            self.atividades.add(atividade)
            self.valor += atividade.valor
        else:
            raise Exception("atividade nao adicionada")

    def aplicar_cupom(self, cupom):
        if cupom.validade_cupom():
            self.valor -= self.valor*cupom.desconto
        else:
            raise Exception("Cupom nao e valido  ")

    def get_atividades(self):
        return self.evento.atividades


class Item_Inscricao(models.Model):
    inscricao = models.ForeignKey(Inscricao, on_delete=models.CASCADE, related_name='item_inscricao')
    atividade = models.ForeignKey('core.Atividade', on_delete=models.CASCADE, related_name='item_inscrisao')
    horario = models.TimeField()
    check_in = models.ForeignKey('core.Check_in', on_delete=models.CASCADE, related_name='item_inscricao')