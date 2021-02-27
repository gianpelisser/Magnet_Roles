-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 27-Fev-2021 às 08:50
-- Versão do servidor: 10.4.17-MariaDB
-- versão do PHP: 7.4.13

START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `magnetroles`
--
CREATE DATABASE IF NOT EXISTS `magnetroles` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE magnetroles;

-- --------------------------------------------------------

--
-- Estrutura da tabela `d_roles`
--

CREATE TABLE `d_roles` (
  `id_role` int(11) NOT NULL,
  `id_server` int(11) NOT NULL,
  `discord_id` bigint(20) NOT NULL,
  `discord_nome` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `role_id` bigint(20) NOT NULL,
  `user_ban` varchar(20) COLLATE utf8_unicode_ci DEFAULT 'no',
  `role_ban` varchar(20) COLLATE utf8_unicode_ci DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Truncar tabela antes do insert `d_roles`
--

TRUNCATE TABLE `d_roles`;
-- --------------------------------------------------------

--
-- Estrutura da tabela `d_roles_adm`
--

CREATE TABLE `d_roles_adm` (
  `id_role_adm` int(11) NOT NULL,
  `id_server` int(11) NOT NULL,
  `role_id_adm` bigint(20) NOT NULL,
  `role_name_adm` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `role_can_use` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Truncar tabela antes do insert `d_roles_adm`
--

TRUNCATE TABLE `d_roles_adm`;
-- --------------------------------------------------------

--
-- Estrutura da tabela `d_servers`
--

CREATE TABLE `d_servers` (
  `id_server` int(11) NOT NULL,
  `server_id` bigint(20) NOT NULL,
  `server_nome` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `server_prefix` varchar(10) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'mr',
  `server_ativo` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'yes',
  `on_member_join` varchar(20) COLLATE utf8_unicode_ci DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Truncar tabela antes do insert `d_servers`
--

TRUNCATE TABLE `d_servers`;
--
-- Extraindo dados da tabela `d_servers`
--

INSERT INTO `d_servers` (`id_server`, `server_id`, `server_nome`, `server_prefix`, `server_ativo`, `on_member_join`) VALUES
(1, 815112299898601474, 'ÍMÃ DE CARGOS [BOT]', 'mr', 'yes', 'yes'),
(2, 605389794641707018, 'S.A.S - Slots System', 'mr', 'yes', 'no');

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `d_roles`
--
ALTER TABLE `d_roles`
  ADD PRIMARY KEY (`id_role`),
  ADD KEY `id_server` (`id_server`);

--
-- Índices para tabela `d_roles_adm`
--
ALTER TABLE `d_roles_adm`
  ADD PRIMARY KEY (`id_role_adm`);

--
-- Índices para tabela `d_servers`
--
ALTER TABLE `d_servers`
  ADD PRIMARY KEY (`id_server`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `d_roles`
--
ALTER TABLE `d_roles`
  MODIFY `id_role` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `d_roles_adm`
--
ALTER TABLE `d_roles_adm`
  MODIFY `id_role_adm` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `d_servers`
--
ALTER TABLE `d_servers`
  MODIFY `id_server` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restrições para despejos de tabelas
--

--
-- Limitadores para a tabela `d_roles`
--
ALTER TABLE `d_roles`
  ADD CONSTRAINT `id_server` FOREIGN KEY (`id_server`) REFERENCES `d_servers` (`id_server`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
