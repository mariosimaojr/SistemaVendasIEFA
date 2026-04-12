-- =============================================================
-- AJUSTES ESTRUTURAIS DO BANCO controle_vendas_iefa
-- =============================================================

-- 1) PADRONIZAR CHARSET E COLLATE NO BANCO

ALTER DATABASE controle_vendas_iefa
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


-- =============================================================
-- 2) PADRONIZAR CHARSET E COLLATE NAS TABELAS
-- =============================================================

ALTER TABLE categorias CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
ALTER TABLE produtos CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
ALTER TABLE usuarios CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
ALTER TABLE vendas CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
ALTER TABLE venda_itens CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
ALTER TABLE movimentacoes_estoque CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- =============================================================
-- 3) REMOVER FK E CAMPO SEQCLIENTE (tabela clientes removida)
-- =============================================================

ALTER TABLE vendas
DROP FOREIGN KEY fk_venda_cliente;

ALTER TABLE vendas
DROP INDEX fk_venda_cliente_idx;

ALTER TABLE vendas
DROP COLUMN SEQCLIENTE;

-- =============================================================
-- 4) REMOVER TABELA cliente
-- =============================================================

DROP TABLE cliente;

-- =============================================================
-- 5) PADRONIZAR CAMPOS DE DATA PARA DATETIME
-- =============================================================

ALTER TABLE produtos
MODIFY DATA_CADASTRO DATETIME NOT NULL;

ALTER TABLE vendas
MODIFY DATA_VENDA DATETIME NOT NULL;

ALTER TABLE movimentacoes_estoque
MODIFY DATA_MOVIMENTO DATETIME NOT NULL;

ALTER TABLE usuarios
MODIFY DATA_CRIACAO DATETIME NOT NULL;

-- =============================================================
-- 6) RECRIAR FOREIGN KEYS COM ON DELETE RESTRICT
-- =============================================================

-- PRODUTOS -> CATEGORIAS

ALTER TABLE produtos
DROP FOREIGN KEY fk_categoria;

ALTER TABLE produtos
ADD CONSTRAINT fk_produtos_categoria
FOREIGN KEY (SEQCATEGORIA)
REFERENCES categorias (SEQUENCIA)
ON DELETE RESTRICT
ON UPDATE CASCADE;


-- MOVIMENTACOES -> PRODUTOS

ALTER TABLE movimentacoes_estoque
DROP FOREIGN KEY fk_mov_estoque_produto;

ALTER TABLE movimentacoes_estoque
ADD CONSTRAINT fk_mov_estoque_produto
FOREIGN KEY (SEQPRODUTO)
REFERENCES produtos (SEQUENCIA)
ON DELETE RESTRICT
ON UPDATE CASCADE;


-- MOVIMENTACOES -> USUARIOS

ALTER TABLE movimentacoes_estoque
DROP FOREIGN KEY fk_mov_estoque_usuario;

ALTER TABLE movimentacoes_estoque
ADD CONSTRAINT fk_mov_estoque_usuario
FOREIGN KEY (SEQUSUARIO)
REFERENCES usuarios (SEQUENCIA)
ON DELETE RESTRICT
ON UPDATE CASCADE;


-- VENDAS -> USUARIOS

ALTER TABLE vendas
DROP FOREIGN KEY fk_venda_usuario;

ALTER TABLE vendas
ADD CONSTRAINT fk_venda_usuario
FOREIGN KEY (SEQUSUARIO)
REFERENCES usuarios (SEQUENCIA)
ON DELETE RESTRICT
ON UPDATE CASCADE;


-- VENDA_ITENS -> VENDAS

ALTER TABLE venda_itens
DROP FOREIGN KEY fk_venda;

ALTER TABLE venda_itens
ADD CONSTRAINT fk_venda_itens_venda
FOREIGN KEY (SEQVENDA)
REFERENCES vendas (SEQUENCIA)
ON DELETE RESTRICT
ON UPDATE CASCADE;


-- VENDA_ITENS -> PRODUTOS

ALTER TABLE venda_itens
DROP FOREIGN KEY fk_venda_produto;

ALTER TABLE venda_itens
ADD CONSTRAINT fk_venda_itens_produto
FOREIGN KEY (SEQPRODUTO)
REFERENCES produtos (SEQUENCIA)
ON DELETE RESTRICT
ON UPDATE CASCADE;

-- =============================================================
-- 7) AJUSTE DO CAMPO tipo_movimento
-- =============================================================

ALTER TABLE movimentacoes_estoque
MODIFY TIPO_MOVIMENTO ENUM('ENTRADA','SAIDA') NOT NULL;


-- =============================================================
-- 8) BOAS PRÁTICAS - DEFAULTS
-- =============================================================

ALTER TABLE categorias
MODIFY ATIVO TINYINT NOT NULL DEFAULT 1;

ALTER TABLE produtos
MODIFY ATIVO TINYINT NOT NULL DEFAULT 1;

ALTER TABLE usuarios
MODIFY ATIVO TINYINT NOT NULL DEFAULT 1;


-- =============================================================
-- 9) BOAS PRÁTICAS - AJUSTE DE CAMPO BLOB PARA TEXT
-- =============================================================

ALTER TABLE categorias
MODIFY COLUMN DESCRICAO TEXT;

ALTER TABLE produtos
MODIFY COLUMN DESCRICAO TEXT;

ALTER TABLE movimentacoes_estoque
MODIFY COLUMN OBSERVACAO TEXT;

ALTER TABLE vendas
MODIFY COLUMN OBSERVACOES TEXT;

-- =============================================================
-- 10) BOAS PRÁTICAS - PARONIZACAO DE NOMES DE CAMPOS (SINGULAR)
-- =============================================================

ALTER TABLE vendas
CHANGE COLUMN OBSERVACOES OBSERVACAO TEXT;

ALTER TABLE produtos
CHANGE COLUMN CARACTERISTICAS CARACTERISTICA TEXT;

ALTER TABLE vendas
CHANGE COLUMN DESCONTOS DESCONTO DECIMAL(10,2);

COMMIT;