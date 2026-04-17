from django.db import models
from apps.produtos.models import Produto
from apps.usuarios.models import Usuario


class MovimentacaoEstoque(models.Model):

    TIPO_MOVIMENTO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]

    sequencia = models.IntegerField(
        db_column='SEQUENCIA',
        primary_key=True
    )

    produto = models.ForeignKey(
        Produto,
        db_column='SEQPRODUTO',
        on_delete=models.RESTRICT
    )

    quantidade = models.IntegerField(
        db_column='QUANTIDADE'
    )

    data_movimento = models.DateTimeField(
        db_column='DATA_MOVIMENTO'
    )

    observacao = models.TextField(
        db_column='OBSERVACAO',
        null=True,
        blank=True
    )

    usuario = models.ForeignKey(
        Usuario,
        db_column='SEQUSUARIO',
        on_delete=models.RESTRICT
    )

    tipo_movimento = models.CharField(
        db_column='TIPO_MOVIMENTO',
        max_length=20,
        choices=TIPO_MOVIMENTO_CHOICES
    )

    class Meta:
        db_table = 'movimentacoes_estoque'
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data_movimento']
        managed = False

    def __str__(self):
        return f'{self.tipo_movimento} - {self.produto.nome} - {self.quantidade}'