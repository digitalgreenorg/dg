-- Normalized version of digitalgreen.SCREENING
DROP TABLE IF EXISTS `screening_myisam`;
CREATE TABLE `screening_myisam` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `screening_id` bigint(20) unsigned NOT NULL,
  `date` date NOT NULL,
  `video_id` bigint(20) unsigned DEFAULT NULL,
  `practice_id` bigint(20) unsigned DEFAULT NULL,
  `group_id` bigint(20) unsigned DEFAULT NULL,
  `village_id` bigint(20) unsigned DEFAULT NULL,
  `block_id` bigint(20) unsigned DEFAULT NULL,
  `district_id` bigint(20) unsigned DEFAULT NULL,
  `state_id` bigint(20) unsigned DEFAULT NULL,
  `country_id` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
CREATE INDEX screening_myisam_screening_id ON screening_myisam(screening_id);
CREATE INDEX screening_myisam_video_id ON screening_myisam(video_id);
CREATE INDEX screening_myisam_practice_id ON screening_myisam(practice_id);
CREATE INDEX screening_myisam_group_id ON screening_myisam(group_id);
CREATE INDEX screening_myisam_date ON screening_myisam(date);
CREATE INDEX screening_myisam_village_id ON screening_myisam(village_id, date);
CREATE INDEX screening_myisam_block_id ON screening_myisam(block_id, date);
CREATE INDEX screening_myisam_district_id ON screening_myisam(district_id, date);
CREATE INDEX screening_myisam_country_id ON screening_myisam(country_id, date);


-- Normalized version of digitalgreen.VIDEO
DROP TABLE IF EXISTS `video_myisam`;
CREATE TABLE `video_myisam` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `video_id` bigint(20) unsigned NOT NULL,
  `video_production_end_date` date NOT NULL,
  `prod_duration` int(5) DEFAULT NULL,
  `practice_id` bigint(20) unsigned DEFAULT NULL,
  `video_type` int(11) NOT NULL,
  `language_id` bigint(20) unsigned DEFAULT NULL,
  `actor_id` bigint(20) unsigned DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `actor_type` varchar(1) NOT NULL,
  `village_id` bigint(20) unsigned DEFAULT NULL,
  `block_id` bigint(20) unsigned DEFAULT NULL,
  `district_id` bigint(20) unsigned DEFAULT NULL,
  `state_id` bigint(20) unsigned DEFAULT NULL,
  `country_id` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
CREATE INDEX video_myisam_video_id ON video_myisam(video_id);
CREATE INDEX video_myisam_practice_id ON video_myisam(practice_id);
CREATE INDEX video_myisam_language_id ON video_myisam(language_id);
CREATE INDEX video_myisam_actor_id ON video_myisam(actor_id);
CREATE INDEX video_myisam_date ON video_myisam(video_production_end_date);
CREATE INDEX video_myisam_village_id ON video_myisam(village_id, video_production_end_date);
CREATE INDEX video_myisam_block_id ON video_myisam(block_id, video_production_end_date);
CREATE INDEX video_myisam_district_id ON video_myisam(district_id, video_production_end_date);
CREATE INDEX video_myisam_country_id ON video_myisam(country_id, video_production_end_date);


-- Normalized version of digitalgreen.PERSON_MEETING_ATTENDANCE
DROP TABLE IF EXISTS `person_meeting_attendance_myisam`;
CREATE TABLE `person_meeting_attendance_myisam` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `pma_id` bigint(20) unsigned NOT NULL,
  `person_id` bigint(20) unsigned DEFAULT NULL,
  `screening_id` bigint(20) unsigned DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `date` date NOT NULL,
  `village_id` bigint(20) unsigned DEFAULT NULL,
  `block_id` bigint(20) unsigned DEFAULT NULL,
  `district_id` bigint(20) unsigned DEFAULT NULL,
  `state_id` bigint(20) unsigned DEFAULT NULL,
  `country_id` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX person_meeting_attendance_myisam_pma_id ON person_meeting_attendance_myisam(pma_id);
CREATE INDEX person_meeting_attendance_myisam_person_id ON person_meeting_attendance_myisam(person_id);
CREATE INDEX person_meeting_attendance_myisam_screening_id ON person_meeting_attendance_myisam(screening_id);
CREATE INDEX person_meeting_attendance_myisam_date ON person_meeting_attendance_myisam(date);
CREATE INDEX person_meeting_attendance_myisam_village_id ON person_meeting_attendance_myisam(village_id, date);
CREATE INDEX person_meeting_attendance_myisam_block_id ON person_meeting_attendance_myisam(block_id, date);
CREATE INDEX person_meeting_attendance_myisam_district_id ON person_meeting_attendance_myisam(district_id, date);
CREATE INDEX person_meeting_attendance_myisam_country_id ON person_meeting_attendance_myisam(country_id, date);

-- Normalized version of digitalgreen.PERSON_ADOPT_PRACTICE
DROP TABLE IF EXISTS `person_adopt_practice_myisam`;
CREATE TABLE `person_adopt_practice_myisam` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `adoption_id` bigint(20) unsigned NOT NULL,
  `person_id` bigint(20) unsigned DEFAULT NULL,
  `video_id` bigint(20) unsigned DEFAULT NULL,
  `practice_id` bigint(20) unsigned DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `date_of_adoption` date NOT NULL,
  `village_id` bigint(20) unsigned DEFAULT NULL,
  `block_id` bigint(20) unsigned DEFAULT NULL,
  `district_id` bigint(20) unsigned DEFAULT NULL,
  `state_id` bigint(20) unsigned DEFAULT NULL,
  `country_id` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX person_adopt_practice_myisam_adoption_id ON person_adopt_practice_myisam(adoption_id);
CREATE INDEX person_adopt_practice_myisam_person_id ON person_adopt_practice_myisam(person_id);
CREATE INDEX person_adopt_practice_myisam_video_id ON person_adopt_practice_myisam(video_id);
CREATE INDEX person_adopt_practice_myisam_practice_id ON person_adopt_practice_myisam(practice_id);
CREATE INDEX person_adopt_practice_myisam_date ON person_adopt_practice_myisam(date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_village_id ON person_adopt_practice_myisam(village_id, date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_block_id ON person_adopt_practice_myisam(block_id, date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_district_id ON person_adopt_practice_myisam(district_id, date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_country_id ON person_adopt_practice_myisam(country_id, date_of_adoption);

-- Aggregation of some statistics on a per day per village basis. The _copy derives from an existing table
DROP TABLE IF EXISTS `village_precalculation_copy`;
CREATE TABLE `village_precalculation_copy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_screening` int(10) unsigned NOT NULL DEFAULT '0',
  `total_videos_produced` int(10) unsigned NOT NULL DEFAULT '0',
  `total_male_actors` int(10) unsigned NOT NULL DEFAULT '0',
  `total_female_actors` int(10) unsigned NOT NULL DEFAULT '0',
  `total_adoption` int(10) unsigned NOT NULL DEFAULT '0',
  `total_male_adoptions` int(10) unsigned NOT NULL DEFAULT '0',
  `total_female_adoptions` int(10) unsigned NOT NULL DEFAULT '0',
  `total_attendance` int(10) unsigned NOT NULL DEFAULT '0',
  `total_male_attendance` int(10) unsigned NOT NULL DEFAULT '0',
  `total_female_attendance` int(10) unsigned NOT NULL DEFAULT '0',
  `total_expected_attendance` int(10) unsigned NOT NULL DEFAULT '0',
  `total_expressed_adoption` int(10) unsigned NOT NULL DEFAULT '0',
  `total_interested` int(10) unsigned NOT NULL DEFAULT '0',
  `total_questions_asked` int(10) unsigned NOT NULL DEFAULT '0',
  `total_adopted_attendees` int(10) unsigned NOT NULL DEFAULT '0',
  `total_active_attendees` int(10) unsigned NOT NULL DEFAULT '0',
  `total_adoption_by_active` int(10) unsigned NOT NULL DEFAULT '0',
  `total_video_seen_by_active` int(10) unsigned NOT NULL DEFAULT '0',
  `village_id` bigint(20) unsigned DEFAULT NULL,
  `block_id` bigint(20) unsigned DEFAULT NULL,
  `district_id` bigint(20) unsigned DEFAULT NULL,
  `state_id` bigint(20) unsigned DEFAULT NULL,
  `country_id` bigint(20) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `village_precalculation_village_id_2919c23_uniq` (`village_id`,`date`),
  KEY `village_precalculation_1290e829` (`village_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX village_precalculation_copy_date ON village_precalculation_copy(date);
CREATE INDEX village_precalculation_copy_village_id ON village_precalculation_copy(village_id, date);
CREATE INDEX village_precalculation_copy_block_id ON village_precalculation_copy(block_id, date);
CREATE INDEX village_precalculation_copy_district_id ON village_precalculation_copy(district_id, date);
CREATE INDEX village_precalculation_copy_country_id ON village_precalculation_copy(country_id, date);