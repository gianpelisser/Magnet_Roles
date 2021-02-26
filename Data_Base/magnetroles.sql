-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 17-Fev-2021 às 09:16
-- Versão do servidor: 10.4.17-MariaDB
-- versão do PHP: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `magnetroles`
--

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
-- Extraindo dados da tabela `d_roles`
--

INSERT INTO `d_roles` (`id_role`, `id_server`, `discord_id`, `discord_nome`, `role_id`, `user_ban`, `role_ban`) VALUES
(1, 1, 136933432973459457, 'VORTEX', 809936049781473290, 'no', 'no'),
(3, 1, 136933432973459457, 'VORTEX', 666433572906860554, 'no', 'no'),
(4, 1, 136933432973459457, 'VORTEX', 666433180919922689, 'no', 'no'),
(6, 2, 136933432973459457, 'VORTEX', 810954821246124054, 'no', 'no'),
(7, 2, 136933432973459457, 'VORTEX', 794812834021638145, 'no', 'no'),
(8, 2, 136933432973459457, 'VORTEX', 707658136991039505, 'no', 'no'),
(9, 2, 136933432973459457, 'VORTEX', 740651702189031525, 'no', 'no'),
(10, 2, 136933432973459457, 'VORTEX', 794377439119540244, 'no', 'no'),
(11, 2, 136933432973459457, 'VORTEX', 791027770889076766, 'no', 'no'),
(12, 2, 136933432973459457, 'VORTEX', 719727401139044353, 'no', 'no'),
(13, 2, 136933432973459457, 'VORTEX', 712812324590846031, 'no', 'no'),
(14, 2, 136933432973459457, 'VORTEX', 775189508026794004, 'no', 'no'),
(15, 2, 136933432973459457, 'VORTEX', 740651608186159213, 'no', 'no'),
(16, 2, 136933432973459457, 'VORTEX', 660503335710752779, 'no', 'no'),
(17, 2, 136933432973459457, 'VORTEX', 635674468076879880, 'no', 'no'),
(18, 2, 136933432973459457, 'VORTEX', 635670834975080448, 'no', 'no'),
(19, 2, 136933432973459457, 'VORTEX', 612492758699212813, 'no', 'no'),
(20, 2, 136933432973459457, 'VORTEX', 663081393777278994, 'no', 'no'),
(21, 2, 136933432973459457, 'VORTEX', 612532691761627136, 'no', 'no'),
(22, 2, 136933432973459457, 'VORTEX', 615777852243181569, 'no', 'no'),
(23, 2, 136933432973459457, 'VORTEX', 627932752657907754, 'no', 'no'),
(24, 2, 136933432973459457, 'VORTEX', 653075382400057379, 'no', 'no'),
(25, 1, 136933432973459457, 'VORTEX', 794380370945507349, 'no', 'no'),
(27, 2, 136933432973459457, 'VORTEX', 605389794641707018, 'no', 'no');

-- --------------------------------------------------------

--
-- Estrutura da tabela `d_servers`
--

CREATE TABLE `d_servers` (
  `id_server` int(11) NOT NULL,
  `server_id` bigint(20) NOT NULL,
  `server_nome` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `server_prefix` varchar(10) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'mr',
  `server_ativo` varchar(100) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'yes'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Extraindo dados da tabela `d_servers`
--

INSERT INTO `d_servers` (`id_server`, `server_id`, `server_nome`, `server_prefix`, `server_ativo`) VALUES
(1, 666432152870846474, 'VORTEX', 'mr', 'yes'),
(2, 605389794641707018, 'S.A.S - Slots System', 'mr', 'yes');

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
  MODIFY `id_role` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

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
