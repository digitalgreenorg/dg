DROP TABLE IF EXISTS `loop_aggregated_myisam`;

CREATE TABLE `loop_aggregated_myisam`(
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `aggregator_id` int unsigned NOT NULL,
  `date` date NOT NULL,
  `mandi_id` int unsigned NOT NULL,
  `gaddidar_id` int unsigned NOT NULL,
  `quantity` decimal,
  `amount` decimal,
  `transportation_cost` decimal,
  `farmer_share` decimal,
  `gaddidar_share` decimal,
  `aggregator_incentive` decimal,
  `aggregator_name` varchar(50) NOT NULL,
  `mandi_name` varchar(50) NOT NULL,
  `gaddidar_name` varchar(50) NOT NULL,
  PRIMARY KEY(`id`)
)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1 ;
