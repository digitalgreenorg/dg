DROP TABLE IF EXISTS `screening_myisam`;
CREATE TABLE `screening_myisam` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `screening_id` int unsigned NOT NULL,
  `date` date NOT NULL,
  `video_id` int unsigned DEFAULT NULL,
  `practice_id` int unsigned DEFAULT NULL,
  `group_id` int unsigned DEFAULT NULL,
  `village_id` int unsigned DEFAULT NULL,
  `block_id` int unsigned DEFAULT NULL,
  `district_id` int unsigned DEFAULT NULL,
  `state_id` int unsigned DEFAULT NULL,
  `country_id` int unsigned DEFAULT NULL,
  `partner_id` int unsigned DEFAULT NULL,
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
CREATE INDEX screening_myisam_state_id ON screening_myisam(state_id, date);
CREATE INDEX screening_myisam_country_id ON screening_myisam(country_id, date);

-- Normalized version of digitalgreen.VIDEO
DROP TABLE IF EXISTS `video_myisam`;
CREATE TABLE `video_myisam` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `video_id` int unsigned NOT NULL,
  `video_production_date` date NOT NULL,
  `practice_id` int unsigned DEFAULT NULL,
  `video_type` int(11) NOT NULL,
  `language_id` int unsigned DEFAULT NULL,
  `village_id` int unsigned DEFAULT NULL,
  `block_id` int unsigned DEFAULT NULL,
  `district_id` int unsigned DEFAULT NULL,
  `state_id` int unsigned DEFAULT NULL,
  `country_id` int unsigned DEFAULT NULL,
  `partner_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
CREATE INDEX video_myisam_video_id ON video_myisam(video_id);
CREATE INDEX video_myisam_practice_id ON video_myisam(practice_id);
CREATE INDEX video_myisam_language_id ON video_myisam(language_id);
CREATE INDEX video_myisam_date ON video_myisam(video_production_date);
CREATE INDEX video_myisam_village_id ON video_myisam(village_id, video_production_date);
CREATE INDEX video_myisam_block_id ON video_myisam(block_id, video_production_date);
CREATE INDEX video_myisam_district_id ON video_myisam(district_id, video_production_date);
CREATE INDEX video_myisam_state_id ON video_myisam(state_id, video_production_date);
CREATE INDEX video_myisam_country_id ON video_myisam(country_id, video_production_date);

-- Normalized version of digitalgreen.PERSON_MEETING_ATTENDANCE
DROP TABLE IF EXISTS `person_meeting_attendance_myisam`;
CREATE TABLE `person_meeting_attendance_myisam` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `pma_id` int unsigned NOT NULL,
  `person_id` int unsigned DEFAULT NULL,
  `screening_id` int unsigned DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `date` date NOT NULL,
  `village_id` int unsigned DEFAULT NULL,
  `block_id` int unsigned DEFAULT NULL,
  `district_id` int unsigned DEFAULT NULL,
  `state_id` int unsigned DEFAULT NULL,
  `country_id` int unsigned DEFAULT NULL,
  `partner_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX person_meeting_attendance_myisam_pma_id ON person_meeting_attendance_myisam(pma_id);
CREATE INDEX person_meeting_attendance_myisam_person_id ON person_meeting_attendance_myisam(person_id);
CREATE INDEX person_meeting_attendance_myisam_screening_id ON person_meeting_attendance_myisam(screening_id);
CREATE INDEX person_meeting_attendance_myisam_date ON person_meeting_attendance_myisam(date);
CREATE INDEX person_meeting_attendance_myisam_village_id ON person_meeting_attendance_myisam(village_id, date);
CREATE INDEX person_meeting_attendance_myisam_block_id ON person_meeting_attendance_myisam(block_id, date);
CREATE INDEX person_meeting_attendance_myisam_district_id ON person_meeting_attendance_myisam(district_id, date);
CREATE INDEX person_meeting_attendance_myisam_state_id ON person_meeting_attendance_myisam(state_id, date);
CREATE INDEX person_meeting_attendance_myisam_country_id ON person_meeting_attendance_myisam(country_id, date);

-- Normalized version of digitalgreen.PERSON_ADOPT_PRACTICE
DROP TABLE IF EXISTS `person_adopt_practice_myisam`;
CREATE TABLE `person_adopt_practice_myisam` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `adoption_id` int unsigned NOT NULL,
  `person_id` int unsigned DEFAULT NULL,
  `video_id` int unsigned DEFAULT NULL,
  `gender` varchar(1) NOT NULL,
  `date_of_adoption` date NOT NULL,
  `village_id` int unsigned DEFAULT NULL,
  `block_id` int unsigned DEFAULT NULL,
  `district_id` int unsigned DEFAULT NULL,
  `state_id` int unsigned DEFAULT NULL,
  `country_id` int unsigned DEFAULT NULL,
  `partner_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX person_adopt_practice_myisam_adoption_id ON person_adopt_practice_myisam(adoption_id);
CREATE INDEX person_adopt_practice_myisam_person_id ON person_adopt_practice_myisam(person_id);
CREATE INDEX person_adopt_practice_myisam_video_id ON person_adopt_practice_myisam(video_id);
CREATE INDEX person_adopt_practice_myisam_date ON person_adopt_practice_myisam(date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_village_id ON person_adopt_practice_myisam(village_id, date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_block_id ON person_adopt_practice_myisam(block_id, date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_district_id ON person_adopt_practice_myisam(district_id, date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_state_id ON person_adopt_practice_myisam(state_id, date_of_adoption);
CREATE INDEX person_adopt_practice_myisam_country_id ON person_adopt_practice_myisam(country_id, date_of_adoption);

-- Aggregation of some statistics on a per day per village basis. The _copy derives from an existing table
DROP TABLE IF EXISTS `village_precalculation_copy`;
CREATE TABLE `village_precalculation_copy` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `total_screening` int(10) unsigned NOT NULL DEFAULT '0',
  `total_videos_produced` int(10) unsigned NOT NULL DEFAULT '0',
  `total_adoption` int(10) unsigned NOT NULL DEFAULT '0',
  `total_male_adoptions` int(10) unsigned NOT NULL DEFAULT '0',
  `total_female_adoptions` int(10) unsigned NOT NULL DEFAULT '0',
  `total_attendance` int(10) unsigned NOT NULL DEFAULT '0',
  `total_male_attendance` int(10) unsigned NOT NULL DEFAULT '0',
  `total_female_attendance` int(10) unsigned NOT NULL DEFAULT '0',
  `total_expected_attendance` int(10) unsigned NOT NULL DEFAULT '0',
  `total_questions_asked` int(10) unsigned NOT NULL DEFAULT '0',
  `total_adopted_attendees` int(10) unsigned NOT NULL DEFAULT '0',
  `total_active_attendees` int(10) unsigned NOT NULL DEFAULT '0',
  `total_adoption_by_active` int(10) unsigned NOT NULL DEFAULT '0',
  `total_video_seen_by_active` int(10) unsigned NOT NULL DEFAULT '0',
  `village_id` int unsigned DEFAULT NULL,
  `block_id` int unsigned DEFAULT NULL,
  `district_id` int unsigned DEFAULT NULL,
  `state_id` int unsigned DEFAULT NULL,
  `country_id` int unsigned DEFAULT NULL,
  `partner_id` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `village_precalculation_village_id_2919c23_uniq` (`village_id`,`date`,`partner_id`),
  KEY `village_precalculation_1290e829` (`village_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX village_precalculation_copy_date ON village_precalculation_copy(date);
CREATE INDEX village_precalculation_copy_village_id ON village_precalculation_copy(village_id, date);
CREATE INDEX village_precalculation_copy_block_id ON village_precalculation_copy(block_id, date);
CREATE INDEX village_precalculation_copy_district_id ON village_precalculation_copy(district_id, date);
CREATE INDEX village_precalculation_copy_state_id ON village_precalculation_copy(state_id, date);
CREATE INDEX village_precalculation_copy_country_id ON village_precalculation_copy(country_id, date);

-- Screeingwisedata table for raw_data_analytics
DROP TABLE IF EXISTS `activities_screeningwisedata`;
CREATE TABLE `activities_screeningwisedata` (
  `id` bigint(20) not null AUTO_INCREMENT,
  `user_created_id` INT(11),
  `time_created` DATETIME,
  `user_modified_id` INT(11),
  `time_modified` DATETIME,
  `screening_id` INT(11) default null,
  `old_coco_id` BIGINT(20),
  `screening_date` DATE not null,
  `start_time` TIME not null,
  `location` VARCHAR(200) not null,
  `village_id` INT(11) not null,
  `animator_id` INT(11) not null,
  `partner_id` INT(11) not null,
  `video_id` INT(11),
  `video_title` VARCHAR(200) not null,
  `persongroup_id` INT(11),
  `video_youtubeid` VARCHAR(20),
  PRIMARY KEY (`id`)
)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE INDEX activities_screeningwisedata_screening_id ON activities_screeningwisedata(screening_id);
CREATE INDEX activities_screeningwisedata_village_id ON activities_screeningwisedata(village_id);
CREATE INDEX activities_screeningwisedata_animator_id ON activities_screeningwisedata(animator_id);
CREATE INDEX activities_screeningwisedata_partner_id ON activities_screeningwisedata(partner_id);
CREATE INDEX activities_screeningwisedata_video_id ON activities_screeningwisedata(video_id);

-- Animatorwisedata for raw_data_analytics
DROP TABLE IF EXISTS `people_animatorwisedata`;
CREATE TABLE `people_animatorwisedata` (
  `id` bigint(20) not null AUTO_INCREMENT,
  `user_created_id` int(11),
  `time_created` datetime,
  `user_modified_id` int(11),
  `time_modified` datetime,
  `animator_id` int(11) default null,
  `old_coco_id` BIGINT(20),
  `animator_name` VARCHAR(100),
  `gender` VARCHAR(1),
  `phone_no` VARCHAR(100),
  `partner_id` INT(11),
  `district_id` INT(11),
  `total_adoptions` INT(10),
  `assignedvillage_id` BIGINT(20),
  `start_date` date,
  PRIMARY KEY (`id`)
)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE INDEX people_animatorwisedata_animator_id ON people_animatorwisedata(animator_id);
CREATE INDEX people_animatorwisedata_assignedvillage_id ON people_animatorwisedata(assignedvillage_id);

-- Geographies-Partner Added for raw_data_analytics --
DROP TABLE IF EXISTS `village_partner_myisam`;
CREATE TABLE `village_partner_myisam` (
  `id` bigint(20) not null AUTO_INCREMENT,
  `village_id` int(11) DEFAULT NULL,
  `block_id` int(11) DEFAULT NULL,
  `district_id` int(11) DEFAULT NULL,
  `state_id` int(11) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `partner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE INDEX village_partner_myisam_geographies_partner ON village_partner_myisam(village_id,block_id,district_id,state_id,country_id,partner_id);
CREATE INDEX village_partner_myisam_village_partner ON village_partner_myisam(village_id,partner_id);
CREATE INDEX village_partner_myisam_block_partner ON village_partner_myisam(block_id,partner_id);
CREATE INDEX village_partner_myisam_district_partner ON village_partner_myisam(district_id,partner_id);
CREATE INDEX village_partner_myisam_state_partner ON village_partner_myisam(state_id,partner_id);
CREATE INDEX village_partner_myisam_country_partner ON village_partner_myisam(country_id,partner_id);

INSERT INTO `screening_myisam` SELECT * FROM digitalgreen_clone.screening_myisam;
INSERT INTO `video_myisam` SELECT * FROM digitalgreen_clone.video_myisam;
INSERT INTO `person_meeting_attendance_myisam` SELECT * FROM digitalgreen_clone.person_meeting_attendance_myisam;
INSERT INTO `person_adopt_practice_myisam` SELECT * FROM digitalgreen_clone.person_adopt_practice_myisam;
INSERT INTO `village_precalculation_copy` SELECT * FROM digitalgreen_clone.village_precalculation_copy;
INSERT INTO `activities_screeningwisedata` SELECT * FROM digitalgreen_clone.activities_screeningwisedata;
INSERT INTO `people_animatorwisedata` SELECT * FROM digitalgreen_clone.people_animatorwisedata;
INSERT INTO `village_partner_myisam` SELECT * FROM digitalgreen_clone.village_partner_myisam;
