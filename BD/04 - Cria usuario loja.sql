USE `controle_vendas_iefa`;
SET NAMES utf8mb4;

-- Disable safe updates for the current session
SET SQL_SAFE_UPDATES = 0;

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
    'fb70259fede1321f31bf1a52ea5216dea2449e27',
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
    `SENHA_HASH` = 'fb70259fede1321f31bf1a52ea5216dea2449e27',
    `PERFIL` = 'Administrador',
    `ATIVO` = 1
WHERE `LOGIN_ACESSO` = 'loja';

COMMIT;
