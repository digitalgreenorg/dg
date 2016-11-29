/* Deleting data from past one year from all myisam tables*/
DELETE 
FROM 
	`screening_myisam` 
WHERE date >= 20161001;

DELETE
FROM
	`video_myisam`
WHERE `video_production_date` >= 20161001;

DELETE
FROM
	`person_meeting_attendance_myisam`
WHERE `date` >= 20161001;

DELETE
FROM
	`person_adopt_practice_myisam`
WHERE  `date_of_adoption` >= 20161001;

DELETE
FROM
	`activities_screeningwisedata`
WHERE `screening_date`  >= 20161001;

DELETE
FROM
	`people_animatorwisedata`
WHERE `time_created`  >= 20161001;

DELETE
FROM
	`village_precalculation_copy`
WHERE `date` >= 20161001;