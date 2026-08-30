-- Ajuste historico de baixa de estoque das vendas.
-- Base analisada: dump controle_vendas_iefa_20260829_091727.sql.
--
-- Totais esperados para o recorte historico deste ajuste:
--   - 193 itens de venda
--   - 245 unidades vendidas
--   - 193 movimentacoes SAIDA a criar, totalizando -245 em QUANTIDADE
--
-- O script e idempotente para as baixas automaticas que cria, usando o texto
-- padronizado de OBSERVACAO para nao inserir a mesma baixa duas vezes.

SET NAMES utf8mb4;

USE controle_vendas_iefa;

-- Conferencia antes da execucao: base historica coberta pelo ajuste.
SELECT
    COUNT(*) AS itens_venda_historicos,
    COALESCE(SUM(vi.QUANTIDADE), 0) AS unidades_vendidas_historicas
FROM venda_itens vi
INNER JOIN vendas v
    ON v.SEQUENCIA = vi.SEQVENDA
WHERE
    v.SEQUENCIA <= 162
    AND vi.SEQUENCIA <= 206;

-- Conferencia antes da execucao: baixas automaticas ja existentes.
SELECT
    COUNT(*) AS baixas_automaticas_existentes,
    COALESCE(SUM(me.QUANTIDADE), 0) AS quantidade_baixas_automaticas_existentes
FROM movimentacoes_estoque me
WHERE
    me.TIPO_MOVIMENTO = 'SAIDA'
    AND me.OBSERVACAO LIKE 'Baixa automática da venda #% - item #%.';

-- Conferencia antes da execucao: baixas automaticas ainda pendentes.
SELECT
    COUNT(*) AS baixas_automaticas_pendentes,
    COALESCE(SUM(vi.QUANTIDADE), 0) AS unidades_pendentes_para_baixa
FROM venda_itens vi
INNER JOIN vendas v
    ON v.SEQUENCIA = vi.SEQVENDA
WHERE
    v.SEQUENCIA <= 162
    AND vi.SEQUENCIA <= 206
    AND NOT EXISTS (
        SELECT 1
        FROM movimentacoes_estoque me
        WHERE
            me.TIPO_MOVIMENTO = 'SAIDA'
            AND me.OBSERVACAO = CONCAT(
                'Baixa automática da venda #',
                v.SEQUENCIA,
                ' - item #',
                vi.SEQUENCIA,
                '.'
            )
    );

START TRANSACTION;

INSERT INTO movimentacoes_estoque
    (
        SEQPRODUTO,
        QUANTIDADE,
        DATA_MOVIMENTO,
        OBSERVACAO,
        SEQUSUARIO,
        TIPO_MOVIMENTO
    )
SELECT
    vi.SEQPRODUTO,
    -ABS(vi.QUANTIDADE),
    CAST(v.DATA_VENDA AS DATETIME),
    CONCAT(
        'Baixa automática da venda #',
        v.SEQUENCIA,
        ' - item #',
        vi.SEQUENCIA,
        '.'
    ),
    v.SEQUSUARIO,
    'SAIDA'
FROM venda_itens vi
INNER JOIN vendas v
    ON v.SEQUENCIA = vi.SEQVENDA
WHERE
    v.SEQUENCIA <= 162
    AND vi.SEQUENCIA <= 206
    AND NOT EXISTS (
        SELECT 1
        FROM movimentacoes_estoque me
        WHERE
            me.TIPO_MOVIMENTO = 'SAIDA'
            AND me.OBSERVACAO = CONCAT(
                'Baixa automática da venda #',
                v.SEQUENCIA,
                ' - item #',
                vi.SEQUENCIA,
                '.'
            )
    );

SELECT ROW_COUNT() AS movimentacoes_saida_inseridas;

COMMIT;

-- Validacao depois da execucao: baixas automaticas criadas/existentes.
SELECT
    COUNT(*) AS baixas_automaticas_total,
    COALESCE(SUM(me.QUANTIDADE), 0) AS quantidade_baixas_automaticas_total
FROM movimentacoes_estoque me
WHERE
    me.TIPO_MOVIMENTO = 'SAIDA'
    AND me.OBSERVACAO LIKE 'Baixa automática da venda #% - item #%.';

-- Validacao depois da execucao: deve retornar zero pendencias.
SELECT
    COUNT(*) AS itens_venda_sem_baixa_automatica,
    COALESCE(SUM(vi.QUANTIDADE), 0) AS unidades_sem_baixa_automatica
FROM venda_itens vi
INNER JOIN vendas v
    ON v.SEQUENCIA = vi.SEQVENDA
WHERE
    v.SEQUENCIA <= 162
    AND vi.SEQUENCIA <= 206
    AND NOT EXISTS (
        SELECT 1
        FROM movimentacoes_estoque me
        WHERE
            me.TIPO_MOVIMENTO = 'SAIDA'
            AND me.OBSERVACAO = CONCAT(
                'Baixa automática da venda #',
                v.SEQUENCIA,
                ' - item #',
                vi.SEQUENCIA,
                '.'
            )
    );
