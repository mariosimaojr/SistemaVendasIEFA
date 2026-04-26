USE controle_vendas_iefa;

-- ============================================
-- 1) Renomear tabela formapagamento -> formaspagamento
-- ============================================

RENAME TABLE formapagamento TO formaspagamento;


-- ============================================
-- 2) Ajustar campo de vendas:
--    FORMA_PAGAMENTO -> SEQFORMAPAGAMENTO
-- ============================================

ALTER TABLE vendas
CHANGE COLUMN FORMA_PAGAMENTO SEQFORMAPAGAMENTO INT NOT NULL;

-- ============================================
-- 2.1) Ajustar o tipo da coluna filha
-- ============================================

ALTER TABLE vendas
MODIFY COLUMN SEQFORMAPAGAMENTO INT UNSIGNED NOT NULL;

-- ============================================
-- 3) Criar índice para a nova FK
-- ============================================

ALTER TABLE vendas
ADD INDEX idx_vendas_seqformapagamento (SEQFORMAPAGAMENTO);


-- ============================================
-- 4) Criar FK vendas -> formaspagamento
-- ============================================

ALTER TABLE vendas
ADD CONSTRAINT fk_vendas_formaspagamento
FOREIGN KEY (SEQFORMAPAGAMENTO)
REFERENCES formaspagamento (SEQUENCIA)
ON DELETE RESTRICT
ON UPDATE CASCADE;

-- ============================================
-- 5) Corrigir campo com caractere estranho -> produtos preco_venda
-- ============================================


ALTER TABLE produtos
CHANGE COLUMN `PRECO_VENDA` PRECO_VENDA DECIMAL(10,2) NOT NULL;

COMMIT;

-- ============================================
-- 6) Corrigir campo DATA_VENDA para apenas Date -> não DateTime
-- ============================================

ALTER TABLE vendas
MODIFY COLUMN DATA_VENDA DATE NOT NULL;