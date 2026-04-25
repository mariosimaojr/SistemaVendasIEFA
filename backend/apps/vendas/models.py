from django.db import models
from apps.usuarios.models import Usuario
from apps.formaspagamento.models import FormaPagamento
from apps.produtos.models import Produto


class Venda(models.Model):

    sequencia = models.AutoField(
        db_column='SEQUENCIA',
        primary_key=True
    )

    data_venda = models.DateTimeField(
        db_column='DATA_VENDA'
    )

    usuario = models.ForeignKey(
        Usuario,
        db_column='SEQUSUARIO',
        on_delete=models.RESTRICT
    )

    valor_total = models.DecimalField(
        db_column='VALOR_TOTAL',
        max_digits=10,
        decimal_places=2
    )

    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        db_column='SEQFORMAPAGAMENTO',
        on_delete=models.RESTRICT
    )

    observacao = models.TextField(
        db_column='OBSERVACAO',
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'vendas'
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda']
        managed = False

    def __str__(self):
        return f'Venda #{self.sequencia}'


class VendaItem(models.Model):

    sequencia = models.AutoField(
        db_column='SEQUENCIA',
        primary_key=True
    )

    venda = models.ForeignKey(
        Venda,
        db_column='SEQVENDA',
        on_delete=models.CASCADE,
        related_name='itens'
    )

    produto = models.ForeignKey(
        Produto,
        db_column='SEQPRODUTO',
        on_delete=models.RESTRICT
    )

    quantidade = models.IntegerField(
        db_column='QUANTIDADE'
    )

    preco_unitario = models.DecimalField(
        db_column='PRECO_UNITARIO',
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        db_column='SUBTOTAL',
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = 'venda_itens'
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens da Venda'
        managed = False

    def __str__(self):
        return f'Item #{self.sequencia} - Venda #{self.venda_id}'