-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: controle_vendas_iefa
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE SCHEMA controle_vendas_iefa DEFAULT CHARACTER SET latin1 ;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `SEQUENCIA` int NOT NULL AUTO_INCREMENT,
  `NOME` varchar(100) DEFAULT NULL,
  `DESCRICAO` blob,
  `ATIVO` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`SEQUENCIA`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Controle de categorias';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'TESTE',_binary 'TESTE DESCRTICAO',1);
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `SEQUENCIA` int NOT NULL AUTO_INCREMENT,
  `NOME` varchar(100) NOT NULL,
  `TELCOMERCIAL` varchar(10) DEFAULT NULL,
  `TELCELULAR` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`SEQUENCIA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `formapagamento`
--

DROP TABLE IF EXISTS `formapagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `formapagamento` (
  `SEQUENCIA` int unsigned NOT NULL AUTO_INCREMENT,
  `DESCRICAO` varchar(50) NOT NULL,
  `ATIVO` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`SEQUENCIA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `formapagamento`
--

LOCK TABLES `formapagamento` WRITE;
/*!40000 ALTER TABLE `formapagamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `formapagamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimentacoes_estoque`
--

DROP TABLE IF EXISTS `movimentacoes_estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimentacoes_estoque` (
  `SEQUENCIA` int NOT NULL AUTO_INCREMENT,
  `SEQPRODUTO` int NOT NULL,
  `QUANTIDADE` int NOT NULL,
  `DATA_MOVIMENTO` timestamp NOT NULL,
  `OBSERVACAO` blob,
  `SEQUSUARIO` int NOT NULL,
  `TIPO_MOVIMENTO` varchar(50) NOT NULL,
  PRIMARY KEY (`SEQUENCIA`),
  KEY `SEQPRODUTO_idx` (`SEQPRODUTO`),
  KEY `SEQUSUARIO_idx` (`SEQUSUARIO`),
  CONSTRAINT `fk_mov_estoque_produto` FOREIGN KEY (`SEQPRODUTO`) REFERENCES `produtos` (`SEQUENCIA`),
  CONSTRAINT `fk_mov_estoque_usuario` FOREIGN KEY (`SEQUSUARIO`) REFERENCES `usuarios` (`SEQUENCIA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimentacoes_estoque`
--

LOCK TABLES `movimentacoes_estoque` WRITE;
/*!40000 ALTER TABLE `movimentacoes_estoque` DISABLE KEYS */;
/*!40000 ALTER TABLE `movimentacoes_estoque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produtos`
--

DROP TABLE IF EXISTS `produtos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produtos` (
  `SEQUENCIA` int NOT NULL AUTO_INCREMENT,
  `NOME` varchar(100) DEFAULT NULL,
  `DESCRICAO` blob,
  `SEQCATEGORIA` int NOT NULL,
  `PRECO_VENDA` decimal(10,2) NOT NULL,
  `ATIVO` tinyint NOT NULL DEFAULT '1',
  `DATA_CADASTRO` timestamp NOT NULL,
  PRIMARY KEY (`SEQUENCIA`),
  KEY `SEQCATEGORIA_idx` (`SEQCATEGORIA`),
  CONSTRAINT `fk_categoria` FOREIGN KEY (`SEQCATEGORIA`) REFERENCES `categorias` (`SEQUENCIA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produtos`
--

LOCK TABLES `produtos` WRITE;
/*!40000 ALTER TABLE `produtos` DISABLE KEYS */;
/*!40000 ALTER TABLE `produtos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `SEQUENCIA` int NOT NULL AUTO_INCREMENT,
  `LOGIN_ACESSO` varchar(100) NOT NULL,
  `EMAIL` varchar(100) NOT NULL,
  `SENHA_HASH` varchar(255) NOT NULL,
  `PERFIL` varchar(50) NOT NULL,
  `ATIVO` tinyint NOT NULL,
  `DATA_CRIACAO` timestamp NOT NULL,
  PRIMARY KEY (`SEQUENCIA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venda_itens`
--

DROP TABLE IF EXISTS `venda_itens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venda_itens` (
  `SEQUENCIA` int NOT NULL AUTO_INCREMENT,
  `SEQVENDA` int NOT NULL,
  `SEQPRODUTO` int NOT NULL,
  `QUANTIDADE` int NOT NULL,
  `PRECO_UNITARIO` decimal(10,2) NOT NULL,
  `SUBTOTAL` decimal(10,2) NOT NULL,
  PRIMARY KEY (`SEQUENCIA`),
  KEY `SEQVENDA_idx` (`SEQVENDA`),
  KEY `SEQPRODUTO_idx` (`SEQPRODUTO`),
  CONSTRAINT `fk_venda` FOREIGN KEY (`SEQVENDA`) REFERENCES `vendas` (`SEQUENCIA`),
  CONSTRAINT `fk_venda_produto` FOREIGN KEY (`SEQPRODUTO`) REFERENCES `produtos` (`SEQUENCIA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venda_itens`
--

LOCK TABLES `venda_itens` WRITE;
/*!40000 ALTER TABLE `venda_itens` DISABLE KEYS */;
/*!40000 ALTER TABLE `venda_itens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vendas`
--

DROP TABLE IF EXISTS `vendas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vendas` (
  `SEQUENCIA` int NOT NULL AUTO_INCREMENT,
  `DATA_VENDA` timestamp NOT NULL,
  `SEQUSUARIO` int NOT NULL,
  `VALOR_TOTAL` decimal(10,2) NOT NULL,
  `FORMA_PAGAMENTO` int NOT NULL,
  `OBSERVACOES` blob,
  `SEQCLIENTE` int NOT NULL,
  PRIMARY KEY (`SEQUENCIA`),
  KEY `sequsuario_idx` (`SEQUSUARIO`),
  KEY `fk_venda_cliente_idx` (`SEQCLIENTE`),
  CONSTRAINT `fk_venda_cliente` FOREIGN KEY (`SEQCLIENTE`) REFERENCES `cliente` (`SEQUENCIA`),
  CONSTRAINT `fk_venda_usuario` FOREIGN KEY (`SEQUSUARIO`) REFERENCES `usuarios` (`SEQUENCIA`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vendas`
--

LOCK TABLES `vendas` WRITE;
/*!40000 ALTER TABLE `vendas` DISABLE KEYS */;
/*!40000 ALTER TABLE `vendas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-19 19:16:12
