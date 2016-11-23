DELETE 
FROM 
	`screening_myisam` 
WHERE date BETWEEN DATE_ADD(Now(), Interval -1 year) AND Now();

DELETE
FROM
	`video_myisam`
WHERE `video_production_date` between DATE_ADD(Now(), Interval -1 year) and Now();

DELETE
FROM
	`person_meeting_attendance_myisam`
WHERE `date` between DATE_ADD(Now(), Interval -1 year) and Now();

 /* DELETE  last 1 year Data from person_adopt_practice_myisam*/

DELETE
FROM
	`person_adopt_practice_myisam`
WHERE  `date_of_adoption` between DATE_ADD(Now(), Interval -1 year) and Now();
/*DELETE last 1 year Data from activities_screeningwisedata*/

DELETE
FROM
	`activities_screeningwisedata`
WHERE `screening_date` between DATE_ADD(Now(), Interval -1 year) and Now();

-- DELETE last 1 year Data from people_animatorwisedata

DELETE
FROM
	`people_animatorwisedata`
WHERE `time_created` between DATE_ADD(Now(), Interval -1 year) and Now();


-- DELETE last 1 year Data from village_precalculation_copy

DELETE
FROM
	`village_precalculation_copy`
WHERE `date` between DATE_ADD(Now(), Interval -1 year) and Now();