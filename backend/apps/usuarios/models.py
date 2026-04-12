from django.db import models
from django.utils import timezone

class Usuario(models.Model):

    sequencia = models.IntegerField(
        db_column='SEQUENCIA',
        primary_key=True
    )

    login_acesso = models.CharField(
        db_column='LOGIN_ACESSO',
        max_length=100
    )

    email = models.CharField(
        db_column='EMAIL',
        max_length=100
    )

    senha_hash = models.CharField(
        db_column='SENHA_HASH',
        max_length=255
    )

    perfil = models.CharField(
        db_column='PERFIL',
        max_length=50
    )

    ativo = models.BooleanField(
        db_column='ATIVO',
        default=True
    )

    data_criacao = models.DateTimeField(
        db_column='DATA_CRIACAO',
        default=timezone.now
    )

    class Meta:

        db_table = 'usuarios'

        verbose_name = 'Usuário'

        verbose_name_plural = 'Usuários'

        ordering = ['login_acesso']

        managed = False

    def __str__(self):

        return self.login_acesso