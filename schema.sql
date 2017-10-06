SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `bwauth`
--

-- --------------------------------------------------------

--
-- Table structure for table `bwauths`
--

CREATE TABLE `bwauths` (
  `id` tinyint(4) NOT NULL,
  `name` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bwauths`
--

INSERT INTO `bwauths` (`id`, `name`) VALUES
(1, 'longclaw'),
(2, 'faravahar'),
(3, 'maatuska'),
(4, 'moria1'),
(5, 'maatuska-vanilla');

-- --------------------------------------------------------

--
-- Table structure for table `files`
--

CREATE TABLE `files` (
  `id` int(11) NOT NULL,
  `name` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `relays`
--

CREATE TABLE `relays` (
  `timestamp` int(11) NOT NULL,
  `fingerprint` varbinary(32) NOT NULL,
  `bwauth` tinyint(4) NOT NULL,
  `bw` mediumint(9) NOT NULL,
  `measured_bw` mediumint(9) DEFAULT NULL,
  `measured_at` int(11) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `scanner` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bwauths`
--
ALTER TABLE `bwauths`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `files`
--
ALTER TABLE `files`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `relays`
--
ALTER TABLE `relays`
  ADD PRIMARY KEY (`timestamp`,`fingerprint`,`bwauth`),
  ADD KEY `timestamp` (`timestamp`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bwauths`
--
ALTER TABLE `bwauths`
  MODIFY `id` tinyint(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `files`
--
ALTER TABLE `files`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4328;