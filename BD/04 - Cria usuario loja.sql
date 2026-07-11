USE `controle_vendas_iefa`;
SET NAMES utf8mb4;

START TRANSACTION;

INSERT INTO `usuarios` (
    `LOGIN_ACESSO`,
    `EMAIL`,
    `SENHA_HASH`,
    `PERFIL`,
    `ATIVO`,
    `DATA_CRIACAO`
)
SELECT
    'loja',
    'loja@iefa.local',
    'd6ea442480377983b42ce1424acd26caf3593045',
    'Administrador',
    1,
    NOW()
WHERE NOT EXISTS (
    SELECT 1
    FROM `usuarios`
    WHERE `LOGIN_ACESSO` = 'loja'
);

UPDATE `usuarios`
SET
    `EMAIL` = 'loja@iefa.local',
    `SENHA_HASH` = 'd6ea442480377983b42ce1424acd26caf3593045',
    `PERFIL` = 'Administrador',
    `ATIVO` = 1
WHERE `LOGIN_ACESSO` = 'loja';

COMMIT;
