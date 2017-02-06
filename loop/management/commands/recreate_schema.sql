DROP TABLE IF EXISTS `loop_aggregated_myisam`;

CREATE TABLE `loop_aggregated_myisam`(
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `aggregator_id` int unsigned NOT NULL,
  `date` date NOT NULL,
  PRIMARY KEY(`id`)
)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1 ;
