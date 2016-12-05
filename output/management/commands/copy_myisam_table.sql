/* Copying into screening_myisam */
INSERT INTO `screening_myisam`
SELECT * FROM digitalgreen_clone.screening_myisam;

/* Copying into video_myisam */
INSERT INTO `video_myisam`
SELECT * FROM digitalgreen_clone.video_myisam;

/* Copying into person_meeting_attendance_myisam */
INSERT INTO `person_meeting_attendance_myisam`
SELECT * FROM digitalgreen_clone.person_meeting_attendance_myisam;

/* Copying into person_adopt_practice_myisam */
INSERT INTO `person_adopt_practice_myisam`
SELECT * FROM digitalgreen_clone.person_adopt_practice_myisam;

/* Copying into activities_screeningwisedata */
INSERT INTO `activities_screeningwisedata`
SELECT * FROM digitalgreen_clone.activities_screeningwisedata;

/* Copying into people_animatorwisedata */
INSERT INTO `people_animatorwisedata`
SELECT * FROM digitalgreen_clone.people_animatorwisedata;

/* Copying into village_precalculation_copy */
INSERT INTO `village_precalculation_copy`
SELECT * FROM digitalgreen_clone.village_precalculation_copy;