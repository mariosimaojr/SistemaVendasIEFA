from django.db import models
from apps.categorias.models import Categoria


class Produto(models.Model):

    sequencia = models.IntegerField(
        db_column='SEQUENCIA',
        primary_key=True
    )

    nome = models.CharField(
        db_column='NOME',
        max_length=100
    )

    descricao = models.TextField(
        db_column='DESCRICAO',
        null=True,
        blank=True
    )

    categoria = models.ForeignKey(
        Categoria,
        db_column='SEQCATEGORIA',
        on_delete=models.RESTRICT
    )

    preco_venda = models.DecimalField(
        db_column='PRECO_VENDA',
        max_digits=10,
        decimal_places=2
    )

    ativo = models.BooleanField(
        db_column='ATIVO',
        default=True
    )

    data_cadastro = models.DateTimeField(
        db_column='DATA_CADASTRO'
    )

    class Meta:
        db_table = 'produtos'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']
        managed = False

    def __str__(self):
        return self.nome