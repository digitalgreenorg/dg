/* Deleting data from past one year from all myisam tables*/
DELETE
FROM
	`village_partner_myisam`;

DELETE 
FROM 
	`screening_myisam` 
WHERE date > DATE_ADD(Now(), Interval -1 year);

DELETE
FROM
	`video_myisam`
WHERE `video_production_date` > DATE_ADD(Now(), Interval -1 year);

DELETE
FROM
	`person_meeting_attendance_myisam`
WHERE `date` > DATE_ADD(Now(), Interval -1 year);

DELETE
FROM
	`person_adopt_practice_myisam`
WHERE  `date_of_adoption` > DATE_ADD(Now(), Interval -1 year);

DELETE
FROM
	`activities_screeningwisedata`
WHERE `screening_date`  > DATE_ADD(Now(), Interval -1 year);

DELETE
FROM
	`people_animatorwisedata`;

DELETE
FROM
	`village_precalculation_copy`;
