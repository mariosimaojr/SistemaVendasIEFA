from django.db import models


class FormaPagamento(models.Model):

    sequencia = models.AutoField(
        db_column='SEQUENCIA',
        primary_key=True
    )

    descricao = models.CharField(
        db_column='DESCRICAO',
        max_length=50
    )

    ativo = models.BooleanField(
        db_column='ATIVO',
        default=True
    )

    class Meta:
        db_table = 'formaspagamento'
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['descricao']
        managed = False

    def __str__(self):
        return self.descricao