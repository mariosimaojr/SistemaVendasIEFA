from django.db import models


class Categoria(models.Model):

    sequencia = models.AutoField(
        primary_key=True,
        db_column='SEQUENCIA'
    )

    nome = models.CharField(
        max_length=100,
        db_column='NOME'
    )

    descricao = models.TextField(
        db_column='DESCRICAO'
    )

    ativo = models.BooleanField(
        default=True,
        db_column='ATIVO'
    )

    class Meta:

        db_table = 'categorias'

        verbose_name = 'Categoria'

        verbose_name_plural = 'Categorias'

        ordering = ['nome']

        managed = False

    def __str__(self):

        return self.nome