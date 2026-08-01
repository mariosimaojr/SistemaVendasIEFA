-- Carga incremental de livros a partir dos scans conferidos
-- Produtos: 126
-- Unidades em estoque: 202
-- Este script nao apaga nem atualiza dados existentes.

USE `controle_vendas_iefa`;
SET NAMES utf8mb4;

DROP PROCEDURE IF EXISTS `sp_carga_livros_scans`;

DELIMITER $$

CREATE PROCEDURE `sp_carga_livros_scans`()
BEGIN
    DECLARE v_done INT DEFAULT 0;
    DECLARE v_ordem INT;
    DECLARE v_autor VARCHAR(150);
    DECLARE v_titulo VARCHAR(150);
    DECLARE v_quantidade INT;
    DECLARE v_preco DECIMAL(10,2);
    DECLARE v_seq_categoria_livro INT;
    DECLARE v_seq_usuario_loja INT;
    DECLARE v_seq_produto INT;
    DECLARE v_total_itens INT DEFAULT 0;
    DECLARE v_total_quantidade INT DEFAULT 0;
    DECLARE v_produtos_inseridos INT DEFAULT 0;
    DECLARE v_movimentacoes_inseridas INT DEFAULT 0;

    DECLARE cur_livros CURSOR FOR
        SELECT `ORDEM`, `AUTOR`, `TITULO`, `QUANTIDADE`, `PRECO`
        FROM `tmp_carga_livros_scans`
        ORDER BY `ORDEM`;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        DROP TEMPORARY TABLE IF EXISTS `tmp_carga_livros_scans`;
        RESIGNAL;
    END;

    START TRANSACTION;

    SET v_seq_categoria_livro = (
        SELECT `SEQUENCIA`
        FROM `categorias`
        WHERE `NOME` = 'LIVRO'
        LIMIT 1
    );

    SET v_seq_usuario_loja = (
        SELECT `SEQUENCIA`
        FROM `usuarios`
        WHERE `LOGIN_ACESSO` = 'loja'
        LIMIT 1
    );

    IF v_seq_categoria_livro IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Categoria LIVRO nao encontrada.';
    END IF;

    IF v_seq_usuario_loja IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Usuario loja nao encontrado.';
    END IF;

    DROP TEMPORARY TABLE IF EXISTS `tmp_carga_livros_scans`;

    CREATE TEMPORARY TABLE `tmp_carga_livros_scans` (
        `ORDEM` INT NOT NULL PRIMARY KEY,
        `AUTOR` VARCHAR(150) NOT NULL,
        `TITULO` VARCHAR(150) NOT NULL,
        `QUANTIDADE` INT NOT NULL,
        `PRECO` DECIMAL(10,2) NOT NULL
    ) ENGINE=Memory DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

    INSERT INTO `tmp_carga_livros_scans` (`ORDEM`, `AUTOR`, `TITULO`, `QUANTIDADE`, `PRECO`) VALUES
    (1, 'Divaldo Pereira Franco', 'Grilhões partidos', 1, 50.00),
    (2, 'Francisco Cândido Xavier', 'Há dois mil anos', 1, 60.00),
    (3, 'Waldenir Aparecido Cuin', 'Histórias reais e reflexões', 1, 10.00),
    (4, 'Marcelo Teixeira', 'Inquietações de um espírita', 3, 25.00),
    (5, 'Mário Coelho (org.)', 'Instruções dos espíritos', 1, 39.00),
    (6, 'Caio Ramacciotti', 'Jesus e o Sinédrio', 8, 15.00),
    (7, 'Francisco Cândido Xavier', 'Lázaro redivivo', 1, 50.00),
    (8, 'Pedro de Campos', 'Lentulus: encarnações de Emmanuel', 1, 60.00),
    (9, 'José Carlos de Lucca', 'Levantar e seguir', 1, 25.00),
    (10, 'Francisco Cândido Xavier', 'Levantar e seguir', 1, 25.00),
    (11, 'Não identificado', 'Luz imperecível', 1, 40.00),
    (12, 'Jacob Melo', 'Manual do passista', 2, 50.00),
    (13, 'Alírio de Cerqueira Filho', 'Mediunidade e obsessão', 1, 35.00),
    (14, 'Francisco Cândido Xavier', 'No mundo maior', 1, 50.00),
    (15, 'Carlos Antônio Baccelli', 'No princípio era o verbo', 13, 20.00),
    (16, 'Divaldo Pereira Franco', 'No rumo do mundo de regeneração', 1, 60.00),
    (17, 'Carlos Antônio Baccelli', 'Nos céus da Gália', 1, 37.00),
    (18, 'Marlene Nobre', 'Nossa vida no além', 1, 55.00),
    (19, 'Divaldo Pereira Franco', 'Novos rumos para o centro espírita', 2, 30.00),
    (20, 'Francisco Cândido Xavier', 'O Consolador', 1, 50.00),
    (21, 'Maria de Lourdes Spadin', 'O coração em palavras', 1, 10.00),
    (22, 'Carlos Antônio Baccelli', 'O Cristo consolador', 1, 50.00),
    (23, 'Allan Kardec', 'O evangelho do dia vol. 3', 1, 40.00),
    (24, 'Allan Kardec', 'O evangelho do dia vol. 4', 1, 40.00),
    (25, 'Allan Kardec', 'O evangelho do dia vol. 5', 3, 40.00),
    (26, 'Allan Kardec', 'O evangelho do dia vol. 6', 1, 40.00),
    (27, 'Allan Kardec', 'O evangelho segundo o espiritismo (letra grande)', 2, 60.00),
    (28, 'Allan Kardec', 'O evangelho segundo o espiritismo (reciclados)', 8, 20.00),
    (29, 'Richard Simonetti', 'O grande desafio', 1, 30.00),
    (30, 'Richard Simonetti', 'O homem de bem', 8, 15.00),
    (31, 'Alcione Reis Albuquerque', 'O homem sadio', 2, 45.00),
    (32, 'Allan Kardec', 'O livro dos espíritos', 1, 50.00),
    (33, 'Allan Kardec', 'O livro dos médiuns', 1, 50.00),
    (34, 'Raymundo R. Espelho', 'O pensamento de Herculano Pires', 1, 16.00),
    (35, 'João Nunes Maia', 'O reino de Deus', 1, 35.00),
    (36, 'Allan Kardec', 'Obras póstumas', 2, 50.00),
    (37, 'Edgard Armond', 'Os exilados de Capela', 1, 60.00),
    (38, 'Hermínio Corrêa de Miranda', 'Os procuradores de Deus', 2, 35.00),
    (39, 'Francisco Cândido Xavier', 'Palavras de vida eterna', 1, 35.00),
    (40, 'Francisco Cândido Xavier', 'Pão nosso', 1, 50.00),
    (41, 'Marlene Nobre', 'A alma da matéria', 2, 40.00),
    (42, 'Alexandre Caldino Neto', 'A essência do espiritismo', 1, 50.00),
    (43, 'André Trigueiro', 'A força do um', 1, 39.00),
    (44, 'Vera Lúcia Marinzeck de Carvalho', 'A história de cada um', 2, 35.00),
    (45, 'Carlos Antônio Baccelli', 'A reencarnação para adolescentes', 1, 20.00),
    (46, 'Alexandre Caudini Neto', 'A vida na visão do espiritismo', 1, 40.00),
    (47, 'Francisco Cândido Xavier', 'Agenda cristã', 1, 35.00),
    (48, 'José Carlos de Lucca', 'Alguém me tocou', 1, 50.00),
    (49, 'Adilton Pugliese', 'Allan Kardec e o centro espírita', 2, 30.00),
    (50, 'Francisco Cândido Xavier', 'Alvorada cristã', 1, 60.00),
    (51, 'Beatriz Aquino', 'Amor e abandono', 1, 25.00),
    (52, 'Divaldo Pereira Franco', 'Anotações espíritas', 1, 40.00),
    (53, 'Rafael Siqueira', 'Ao encontro de Jesus', 1, 50.00),
    (54, 'André Luiz Peixinho', 'As bem-aventuranças e outras belezas espirituais', 1, 34.00),
    (55, 'Francisco Cândido Xavier', 'Assembleia de luz', 1, 25.00),
    (56, 'Nena Galves', 'Até sempre Chico Xavier', 2, 30.00),
    (57, 'Neuza Zarponi Melo', 'Atendimento fraterno no centro espírita', 1, 40.00),
    (58, 'Divaldo Pereira Franco', 'Atualidade do pensamento espírita', 1, 15.00),
    (59, 'Augusto Cezar Netto', 'Augusto vive', 1, 15.00),
    (60, 'Francisco Cândido Xavier', 'Ave, Cristo!', 1, 60.00),
    (61, 'Francisco Cândido Xavier', 'Brasil, coração do mundo, pátria do evangelho', 1, 50.00),
    (62, 'Cirinéia Iolanda Maffei', 'Camélias de luz', 3, 50.00),
    (63, 'Francisco Cândido Xavier', 'Caminho, verdade e vida', 1, 55.00),
    (64, 'Hermínio Corrêa de Miranda', 'Candeias na noite escura', 1, 40.00),
    (65, 'Raul Teixeira', 'Cântico da juventude', 1, 35.00),
    (66, 'Haroldo Dutra Dias', 'Celeiro de redenção', 1, 35.00),
    (67, 'Não identificado', 'Chico Xavier: entrevistas', 1, 25.00),
    (68, 'Ubiratan Machado', 'Chico Xavier: uma vida de amor', 3, 25.00),
    (69, 'Hermínio C. De Miranda', 'Com quem tu andas?', 1, 30.00),
    (70, 'Célia Xavier Camargo', 'Comunicação entre dois mundos', 1, 34.00),
    (71, 'Divaldo Pereira Franco', 'Conversa fraterna', 1, 15.00),
    (72, 'Therezinha Oliveira', 'Conversando com os espíritos na reunião mediúnica', 1, 40.00),
    (73, 'Sérgio Cherci', 'Curas espirituais a luz da doutrina espírita', 2, 70.00),
    (74, 'Raul Teixeira', 'Desafios da educação', 2, 35.00),
    (75, 'Yvonne Pereira', 'Devassando o invisível', 3, 45.00),
    (76, 'Francisco Cândido Xavier', 'Diálogo dos vivos', 2, 18.00),
    (77, 'Divaldo Pereira Franco', 'Diretrizes de segurança', 1, 10.00),
    (78, 'Divaldo Pereira Franco', 'Divaldo responde Vol. 2', 1, 50.00),
    (79, 'Francisco Cândido Xavier', 'Doutrina de luz', 1, 13.00),
    (80, 'Carlos Antônio Baccelli', 'Dr. Inácio Ferreira convida você a pensar', 9, 30.00),
    (81, 'Raul Teixeira', 'Em nome de Deus', 1, 15.00),
    (82, 'Adriano Calsone', 'Em nome de Kardec', 1, 25.00),
    (83, 'Yvonne Pereira', 'Entre cartas e recordações', 1, 30.00),
    (84, 'Francisco Cândido Xavier', 'Estante da vida', 1, 50.00),
    (85, 'Chico Xavier e Waldo Vieira', 'Evolução em dois mundos', 2, 50.00),
    (86, 'Raul Teixeira', 'Para uma vida melhor na terra', 1, 15.00),
    (87, 'Francisco Cândido Xavier', 'Pensamento e vida', 2, 25.00),
    (88, 'Walter Oliveira Alves', 'Prática pedagógica na evangelização vol. 2', 1, 20.00),
    (89, 'Walter Oliveira Alves', 'Prática pedagógica na evangelização vol. 3', 1, 32.00),
    (90, 'Divaldo Pereira Franco', 'Quando voltar a primavera', 1, 30.00),
    (91, 'Hernani Guimarães Andrade', 'Reencarnação no Brasil', 1, 50.00),
    (92, 'Durval Ciamponi', 'Reprodução assistida à luz do espiritismo', 1, 10.00),
    (93, 'Therezinha Oliveira', 'Reuniões mediúnicas - vol. 3', 2, 40.00),
    (94, 'Não identificado', 'Revista Espírita: jornal de estudos psicológicos, 1861', 1, 35.00),
    (95, 'Não identificado', 'Revista Espírita: jornal de estudos psicológicos, 1862', 1, 35.00),
    (96, 'Não identificado', 'Revista Espírita: jornal de estudos psicológicos, 1863', 1, 35.00),
    (97, 'Não identificado', 'Revista Espírita: jornal de estudos psicológicos, 1864', 1, 35.00),
    (98, 'Não identificado', 'Revista Espírita: jornal de estudos psicológicos, 1865', 1, 35.00),
    (99, 'Não identificado', 'Revista Espírita: jornal de estudos psicológicos, 1866', 1, 35.00),
    (100, 'Não identificado', 'Revista Espírita: jornal de estudos psicológicos, 1867', 1, 35.00),
    (101, 'Carlos Antônio Baccelli', 'Seara de luz', 1, 15.00),
    (102, 'Kátia Eli Pereira', 'Sempre te amarei', 1, 20.00),
    (103, 'Francisco Cândido Xavier', 'Sexo e destino', 1, 60.00),
    (104, 'Léa Caruso', 'Simão Pedro e os primeiros cristãos', 3, 40.00),
    (105, 'Divaldo Pereira Franco', 'SOS família', 1, 35.00),
    (106, 'Marcel Benedeti', 'Todos os animais merecem o céu', 1, 50.00),
    (107, 'Divaldo Pereira Franco', 'Tormentos da obsessão', 1, 40.00),
    (108, 'Divaldo Pereira Franco', 'Transição planetária', 2, 50.00),
    (109, 'Célia Xavier Camargo', 'Um anjo em nossa vida', 4, 45.00),
    (110, 'Adenauer Novaes', 'Valores do espírito', 1, 45.00),
    (111, 'Francisco Cândido Xavier', 'Vida e sexo', 1, 60.00),
    (112, 'Suely Caldas Schubert', 'Visão espírita para o terceiro milênio', 1, 20.00),
    (113, 'Izaias Claro', 'Viva mais', 1, 25.00),
    (114, 'Antônio Baduy Filho', 'Vivendo o evangelho vol. 2', 2, 35.00),
    (115, 'Não identificado', 'O homem integral', 1, 15.00),
    (116, 'Não identificado', 'Mensagens de Inês de Castro', 2, 50.00),
    (117, 'Não identificado', 'Tremi por dentro', 1, 30.00),
    (118, 'Não identificado', 'Palavras do infinito', 1, 50.00),
    (119, 'Não identificado', 'Todos os animais são nossos irmãos', 1, 50.00),
    (120, 'Não identificado', 'A gotinha de orvalho', 1, 30.00),
    (121, 'Clóvis Tavares', 'Histórias que Jesus contou', 1, 50.00),
    (122, 'Não identificado', 'A conchinha falante', 1, 20.00),
    (123, 'Julieta Marques', 'Uma história de amor', 2, 15.00),
    (124, 'Não identificado', 'A vida de Allan Kardec para crianças', 1, 20.00),
    (125, 'Rita Foelker', 'Uma prova de coragem', 1, 15.00),
    (126, 'Não identificado', 'Jasão, o cego', 1, 15.00);

    SELECT
        COUNT(*),
        COALESCE(SUM(`QUANTIDADE`), 0)
    INTO
        v_total_itens,
        v_total_quantidade
    FROM `tmp_carga_livros_scans`;

    IF v_total_itens <> 126 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validacao falhou: quantidade de produtos diferente de 126.';
    END IF;

    IF v_total_quantidade <> 202 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validacao falhou: soma de estoque diferente de 202.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM `tmp_carga_livros_scans`
        WHERE `QUANTIDADE` <= 0 OR `PRECO` < 0
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validacao falhou: quantidade ou preco invalido.';
    END IF;

    OPEN cur_livros;

    carga_loop: LOOP
        FETCH cur_livros INTO v_ordem, v_autor, v_titulo, v_quantidade, v_preco;

        IF v_done = 1 THEN
            LEAVE carga_loop;
        END IF;

        INSERT INTO `produtos` (
            `NOME`,
            `DESCRICAO`,
            `SEQCATEGORIA`,
            `PRECO_VENDA`,
            `ATIVO`,
            `DATA_CADASTRO`
        ) VALUES (
            v_titulo,
            CONCAT(
                'Origem: carga livros scans; Item: ',
                v_ordem,
                '; Autor: ',
                v_autor,
                '; Titulo: ',
                v_titulo
            ),
            v_seq_categoria_livro,
            v_preco,
            1,
            NOW()
        );

        SET v_seq_produto = LAST_INSERT_ID();
        SET v_produtos_inseridos = v_produtos_inseridos + 1;

        INSERT INTO `movimentacoes_estoque` (
            `SEQPRODUTO`,
            `QUANTIDADE`,
            `DATA_MOVIMENTO`,
            `OBSERVACAO`,
            `SEQUSUARIO`,
            `TIPO_MOVIMENTO`
        ) VALUES (
            v_seq_produto,
            v_quantidade,
            NOW(),
            'Carga inicial de livros a partir dos scans.',
            v_seq_usuario_loja,
            'ENTRADA'
        );

        SET v_movimentacoes_inseridas = v_movimentacoes_inseridas + 1;
    END LOOP;

    CLOSE cur_livros;

    IF v_produtos_inseridos <> 126 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validacao falhou: produtos inseridos diferente de 126.';
    END IF;

    IF v_movimentacoes_inseridas <> 126 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Validacao falhou: movimentacoes inseridas diferente de 126.';
    END IF;

    COMMIT;

    SELECT
        v_produtos_inseridos AS `produtos_inseridos`,
        v_movimentacoes_inseridas AS `movimentacoes_inseridas`,
        v_total_quantidade AS `unidades_estoque`;

    DROP TEMPORARY TABLE IF EXISTS `tmp_carga_livros_scans`;
END$$

DELIMITER ;

CALL `sp_carga_livros_scans`();

DROP PROCEDURE IF EXISTS `sp_carga_livros_scans`;
