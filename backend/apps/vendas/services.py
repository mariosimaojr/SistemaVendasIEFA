from django.utils import timezone

from apps.movimentacoes_estoque.models import MovimentacaoEstoque


def registrar_baixa_estoque_venda_item(item, usuario):
    return MovimentacaoEstoque.objects.create(
        produto=item.produto,
        quantidade=-abs(item.quantidade),
        data_movimento=timezone.now(),
        observacao=(
            f'Baixa automática da venda #{item.venda_id} '
            f'- item #{item.sequencia}.'
        ),
        usuario=usuario,
        tipo_movimento='SAIDA'
    )
