-- phpMyAdmin SQL Dump
-- version 4.5.2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 24, 2016 at 02:59 PM
-- Server version: 5.7.10
-- PHP Version: 5.5.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ooi_datateam`
--

-- --------------------------------------------------------

--
-- Table structure for table `assets`
--

CREATE TABLE `assets` (
  `id` int(11) UNSIGNED NOT NULL,
  `ooi_barcode` varchar(20) DEFAULT NULL,
  `description_of_equipment` text,
  `quant` float DEFAULT NULL,
  `manufacturer` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `manufacturer_serial_no` varchar(30) DEFAULT NULL,
  `firmware_version` varchar(20) DEFAULT NULL,
  `source_of_the_equipment` varchar(20) DEFAULT NULL,
  `whether_title` varchar(20) DEFAULT NULL,
  `location` varchar(20) DEFAULT NULL,
  `room_number` varchar(30) DEFAULT NULL,
  `condition` varchar(20) DEFAULT NULL,
  `acquisition_date` varchar(20) DEFAULT NULL,
  `original_cost` varchar(20) DEFAULT NULL,
  `federal_participation` varchar(20) DEFAULT NULL,
  `comments` text,
  `primary_tag_date` varchar(20) DEFAULT NULL,
  `primary_tag_organization` varchar(20) DEFAULT NULL,
  `primary_institute_asset_tag` varchar(20) DEFAULT NULL,
  `secondary_tag_date` varchar(20) DEFAULT NULL,
  `second_tag_organization` varchar(20) DEFAULT NULL,
  `institute_asset_tag` varchar(20) DEFAULT NULL,
  `doi_tag_date` varchar(20) DEFAULT NULL,
  `doi_tag_organization` varchar(20) DEFAULT NULL,
  `doi_institute_asset_tag` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `calibrations`
--

CREATE TABLE `calibrations` (
  `id` int(11) UNSIGNED NOT NULL,
  `reference_designator` varchar(27) DEFAULT NULL,
  `mooring_barcode` varchar(25) DEFAULT NULL,
  `mooring_serial_number` varchar(25) DEFAULT NULL,
  `deployment_number` smallint(11) DEFAULT NULL,
  `sensor_barcode` varchar(25) DEFAULT NULL,
  `sensor_serial_number` varchar(25) DEFAULT NULL,
  `cc_name` varchar(75) DEFAULT NULL,
  `cc_value` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `data_streams`
--

CREATE TABLE `data_streams` (
  `id` int(11) UNSIGNED NOT NULL,
  `reference_designator` varchar(27) NOT NULL DEFAULT '',
  `instrument_id` int(11) DEFAULT NULL,
  `method` varchar(100) NOT NULL DEFAULT '',
  `stream_name` varchar(100) NOT NULL DEFAULT '',
  `stream_id` int(11) DEFAULT NULL,
  `uframe_route` varchar(100) NOT NULL DEFAULT '',
  `driver` varchar(100) NOT NULL DEFAULT '',
  `parser` varchar(100) NOT NULL DEFAULT '',
  `instrument_type` varchar(20) NOT NULL DEFAULT '',
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `deployments`
--

CREATE TABLE `deployments` (
  `id` int(11) UNSIGNED NOT NULL,
  `reference_designator` varchar(27) DEFAULT NULL,
  `mooring_barcode` varchar(25) DEFAULT NULL,
  `mooring_serial_number` varchar(25) DEFAULT NULL,
  `deployment_number` smallint(11) DEFAULT NULL,
  `anchor_launch_date` date DEFAULT NULL,
  `anchor_launch_time` time DEFAULT NULL,
  `recover_date` date DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `water_depth` float DEFAULT NULL,
  `cruise_number` varchar(50) DEFAULT NULL,
  `notes` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `instruments`
--

CREATE TABLE `instruments` (
  `id` int(11) UNSIGNED NOT NULL,
  `reference_designator` varchar(27) DEFAULT NULL,
  `node_rd` varchar(14) NOT NULL DEFAULT '',
  `name` varchar(75) DEFAULT NULL,
  `start_depth` decimal(6,2) DEFAULT NULL,
  `end_depth` decimal(6,2) DEFAULT NULL,
  `location` varchar(45) DEFAULT NULL,
  `current_status` varchar(10) DEFAULT NULL,
  `uframe_status` varchar(10) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `instrument_classes`
--

CREATE TABLE `instrument_classes` (
  `id` int(11) UNSIGNED NOT NULL,
  `class` varchar(5) NOT NULL DEFAULT '',
  `name` varchar(75) NOT NULL DEFAULT '',
  `description` text,
  `primary_science_dicipline` varchar(50) NOT NULL DEFAULT '',
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `instrument_models`
--

CREATE TABLE `instrument_models` (
  `id` int(11) UNSIGNED NOT NULL,
  `class` varchar(5) NOT NULL DEFAULT '',
  `series` varchar(2) NOT NULL DEFAULT '',
  `name` varchar(75) NOT NULL,
  `make` varchar(50) NOT NULL DEFAULT '',
  `model` varchar(75) NOT NULL DEFAULT '',
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `monthly_stats`
--

CREATE TABLE `monthly_stats` (
  `id` int(11) UNSIGNED NOT NULL,
  `reference_designator` varchar(27) DEFAULT NULL,
  `month` date DEFAULT NULL,
  `uframe_status` tinyint(1) DEFAULT NULL,
  `deployed_status` varchar(10) DEFAULT NULL,
  `casandra_status` tinyint(1) DEFAULT NULL,
  `reviewed_status` varchar(10) DEFAULT NULL,
  `reviewed_user_id` int(11) DEFAULT NULL,
  `reviewed_comment` text,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `nodes`
--

CREATE TABLE `nodes` (
  `id` int(11) UNSIGNED NOT NULL,
  `reference_designator` varchar(14) NOT NULL DEFAULT '',
  `site_rd` varchar(8) NOT NULL DEFAULT '',
  `name` varchar(75) NOT NULL DEFAULT '',
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `notes`
--

CREATE TABLE `notes` (
  `id` int(11) UNSIGNED NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `body` text,
  `type` varchar(10) DEFAULT NULL,
  `model` varchar(20) DEFAULT NULL,
  `reference_designator` varchar(30) DEFAULT NULL,
  `redmine_issue` varchar(20) DEFAULT NULL,
  `resolved` date DEFAULT NULL,
  `resolved_comment` text,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `parameters`
--

CREATE TABLE `parameters` (
  `id` int(11) UNSIGNED NOT NULL,
  `name` varchar(250) CHARACTER SET latin1 DEFAULT NULL,
  `unit` varchar(250) COLLATE utf8_swedish_ci DEFAULT NULL,
  `fill_value` varchar(20) CHARACTER SET latin1 DEFAULT NULL,
  `display_name` varchar(250) COLLATE utf8_swedish_ci DEFAULT NULL,
  `standard_name` varchar(250) CHARACTER SET latin1 DEFAULT NULL,
  `parameter_precision` varchar(10) COLLATE utf8_swedish_ci DEFAULT NULL,
  `parameter_function_id` varchar(250) CHARACTER SET latin1 DEFAULT NULL,
  `parameter_function_map` text CHARACTER SET latin1,
  `data_product_identifier` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `description` text COLLATE utf8_swedish_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `parameters_streams`
--

CREATE TABLE `parameters_streams` (
  `parameter_id` int(11) UNSIGNED NOT NULL,
  `stream_id` int(11) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `parameter_functions`
--

CREATE TABLE `parameter_functions` (
  `id` int(11) UNSIGNED NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `function_type` varchar(20) DEFAULT NULL,
  `function` varchar(250) DEFAULT NULL,
  `owner` varchar(250) DEFAULT NULL,
  `description` text,
  `qc_flag` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `regions`
--

CREATE TABLE `regions` (
  `id` int(11) UNSIGNED NOT NULL,
  `reference_designator` varchar(2) NOT NULL DEFAULT '',
  `name` varchar(75) NOT NULL DEFAULT '',
  `description` text,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sites`
--

CREATE TABLE `sites` (
  `id` int(11) UNSIGNED NOT NULL,
  `reference_designator` varchar(8) NOT NULL DEFAULT '',
  `region_rd` varchar(2) NOT NULL DEFAULT '',
  `array_name` varchar(75) DEFAULT NULL,
  `name` varchar(75) NOT NULL DEFAULT '',
  `description` text,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `bottom_depth` float DEFAULT NULL,
  `current_status` varchar(10) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `streams`
--

CREATE TABLE `streams` (
  `id` int(11) UNSIGNED NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `time_parameter` int(11) DEFAULT NULL,
  `uses_ctd` tinyint(1) DEFAULT NULL,
  `binsize_minutes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(10) UNSIGNED NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `role` varchar(20) DEFAULT NULL,
  `token` varchar(40) DEFAULT NULL,
  `token_expires` datetime DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `modified` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `assets`
--
ALTER TABLE `assets`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ooi_barcode` (`ooi_barcode`);

--
-- Indexes for table `calibrations`
--
ALTER TABLE `calibrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `data_streams`
--
ALTER TABLE `data_streams`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reference_designator` (`reference_designator`,`method`,`stream_name`);

--
-- Indexes for table `deployments`
--
ALTER TABLE `deployments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `instruments`
--
ALTER TABLE `instruments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reference_designator` (`reference_designator`);

--
-- Indexes for table `instrument_classes`
--
ALTER TABLE `instrument_classes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `class` (`class`);

--
-- Indexes for table `instrument_models`
--
ALTER TABLE `instrument_models`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `class_series` (`class`,`series`) USING BTREE;

--
-- Indexes for table `monthly_stats`
--
ALTER TABLE `monthly_stats`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reference_designator_month` (`reference_designator`,`month`) USING BTREE;

--
-- Indexes for table `nodes`
--
ALTER TABLE `nodes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reference_designator` (`reference_designator`);

--
-- Indexes for table `notes`
--
ALTER TABLE `notes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `parameters`
--
ALTER TABLE `parameters`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `parameters_streams`
--
ALTER TABLE `parameters_streams`
  ADD PRIMARY KEY (`parameter_id`,`stream_id`) USING BTREE;

--
-- Indexes for table `parameter_functions`
--
ALTER TABLE `parameter_functions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `regions`
--
ALTER TABLE `regions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reference_designator` (`reference_designator`);

--
-- Indexes for table `sites`
--
ALTER TABLE `sites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reference_designator` (`reference_designator`);

--
-- Indexes for table `streams`
--
ALTER TABLE `streams`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `assets`
--
ALTER TABLE `assets`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `calibrations`
--
ALTER TABLE `calibrations`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `data_streams`
--
ALTER TABLE `data_streams`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `deployments`
--
ALTER TABLE `deployments`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `instruments`
--
ALTER TABLE `instruments`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `instrument_classes`
--
ALTER TABLE `instrument_classes`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `instrument_models`
--
ALTER TABLE `instrument_models`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `monthly_stats`
--
ALTER TABLE `monthly_stats`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `nodes`
--
ALTER TABLE `nodes`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `notes`
--
ALTER TABLE `notes`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `parameters`
--
ALTER TABLE `parameters`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `parameter_functions`
--
ALTER TABLE `parameter_functions`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `regions`
--
ALTER TABLE `regions`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `sites`
--
ALTER TABLE `sites`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `streams`
--
ALTER TABLE `streams`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
