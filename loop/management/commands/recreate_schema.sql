DROP TABLE IF EXISTS `loop_aggregated_myisam`;

CREATE TABLE `loop_aggregated_myisam`(
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `aggregator_id` int unsigned NOT NULL,
  `date` date NOT NULL,
  `mandi_id` int unsigned NOT NULL,
  `gaddidar_id` int unsigned NOT NULL,
  `quantity` decimal(10,3),
  `amount` decimal(10,3),
  `transportation_cost` decimal(10,3),
  `farmer_share` decimal(10,3),
  `gaddidar_share` decimal(10,3),
  `aggregator_incentive` decimal(10,3),
  `aggregator_name` varchar(50) NOT NULL,
  `mandi_name` varchar(50) NOT NULL,
  `gaddidar_name` varchar(50) NOT NULL,
  `cum_distinct_farmer` int unsigned NOT NULL,
  `country_id` int unsigned NOT NULL,
  `state_id` int unsigned NOT NULL,
  PRIMARY KEY(`id`)
)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1 ;

CREATE INDEX loop_aggregated_myisam_date ON loop_aggregated_myisam(date);
CREATE INDEX loop_aggregated_myisam_date_aggregator_mandi ON loop_aggregated_myisam(date,aggregator_id,mandi_id);
CREATE INDEX loop_aggregated_myisam_date_aggregator_mandi_gaddidar ON loop_aggregated_myisam(date,aggregator_id,mandi_id,gaddidar_id);
CREATE INDEX loop_aggregated_myisam_date_country ON loop_aggregated_myisam(date,country_id);
