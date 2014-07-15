from django.conf.urls import patterns, url
from views import get_key_for_user, set_key_for_user, login_view, save_country_online, \
get_countries_online, save_country_offline, save_region_online, get_regions_online, \
save_region_offline, save_state_online, get_states_online, save_state_offline, \
save_fieldofficer_online, get_fieldofficers_online, save_fieldofficer_offline, save_practice_online, \
get_practices_online, save_practice_offline, get_practices_seen_for_person, save_language_online, \
get_languages_online, save_language_offline, save_partner_online, get_partners_online, \
save_partner_offline, save_video_online, get_videos_online, get_videos_seen_for_person, \
save_video_offline, save_personshowninvideo_online, get_personshowninvideo_online, save_personshowninvideo_offline, \
save_developmentmanager_online, get_developmentmanagers_online, save_developmentmanager_offline, \
save_equipment_online, get_equipments_online, save_equipment_offline, save_district_online, get_districts_online, \
save_district_offline, save_block_online, get_blocks_online, get_blocks_for_district_online, \
save_block_offline, save_village_online, get_villages_online, get_villages_for_blocks_online, \
save_village_offline, save_animator_online, get_animators_online, save_animator_offline, \
save_animatorassignedvillage_online, get_animatorassignedvillages_online, save_animatorassignedvillage_offline, \
save_persongroup_online, get_persongroups_online, get_persongroups_for_village_online, save_persongroup_offline, \
save_person_online, get_persons_online, get_person_for_village_and_no_person_group_online, \
get_person_for_person_group_online, save_person_offline, save_screening_online, get_screenings_online, \
save_screening_offline, get_attendance, get_groupstargetedinscreening_online, save_groupstargetedinscreening_offline, \
save_videosscreenedinscreening_online, get_videosscreenedinscreening_online, save_videosscreenedinscreening_offline, \
save_training_online, get_trainings_online, save_training_offline, save_traininganimatorstrained_online, \
get_traininganimatorstrained_online, save_traininganimatorstrained_offline, save_monthlycostpervillage_online, \
get_monthlycostpervillages_online, save_monthlycostpervillage_offline, save_animatorsalarypermonth_online, \
get_animatorsalarypermonths_online, save_animatorsalarypermonth_offline, save_personrelation_online, \
get_personrelations_online, save_personrelation_offline, \
get_personmeetingattendances_online, save_personmeetingattendance_offline, \
save_personadoptpractice_online, get_personadoptpractices_online, save_personadoptpractice_offline, \
save_equipmentholder_online, get_equipmentholders_online, save_equipmentholder_offline, save_reviewer_online, \
get_reviewers_online, save_reviewer_offline, save_target_online, get_targets_online, save_target_offline, \
get_dashboard_errors_online, mark_error_as_not_error, index_template_data, farmers_in_groups, \
persons_in_screening, person_meeting_attendance_data, screenings_in_village, filters_for_village, \
practices_seen_by_farmer, practices_in_videos

urlpatterns = patterns('',
    (r'^getkey/$', get_key_for_user),
    (r'^setkey/$', set_key_for_user),
    (r'^login/$', login_view),
    (r'^savecountryonline/((?P<id>\d*)/)?$', save_country_online),
    (r'^getcountriesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_countries_online),
    (r'^savecountryoffline/((?P<id>\d*)/)?$', save_country_offline),
    (r'^saveregiononline/((?P<id>\d*)/)?$', save_region_online),
    (r'^getregionsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_regions_online),
    (r'^saveregionoffline/((?P<id>\d*)/)?$', save_region_offline),
    (r'^savestateonline/((?P<id>\d*)/)?$', save_state_online),
    (r'^getstatesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_states_online),
    (r'^savestateoffline/((?P<id>\d*)/)?$', save_state_offline),
    (r'^savefieldofficeronline/((?P<id>\d*)/)?$', save_fieldofficer_online),
    (r'^getfieldofficersonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_fieldofficers_online),
    (r'^savefieldofficeroffline/((?P<id>\d*)/)?$', save_fieldofficer_offline),
    (r'^savepracticeonline/((?P<id>\d*)/)?$', save_practice_online),
    (r'^getpracticesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_practices_online),
    (r'^savepracticeoffline/((?P<id>\d*)/)?$', save_practice_offline),
    (r'^getpracticesseenforperson/((?P<person_id>\d*)/)?$', get_practices_seen_for_person),
    (r'^savelanguageonline/((?P<id>\d*)/)?$', save_language_online),
    (r'^getlanguagesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_languages_online),
    (r'^savelanguageoffline/((?P<id>\d*)/)?$', save_language_offline),
    (r'^savepartneronline/((?P<id>\d*)/)?$', save_partner_online),
    (r'^getpartnersonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_partners_online),
    (r'^savepartneroffline/((?P<id>\d*)/)?$', save_partner_offline),
    (r'^savevideoonline/((?P<id>\d*)/)?$', save_video_online),
    (r'^getvideosonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_videos_online),
    (r'^getvideosseenforperson/((?P<person_id>\d*)/)?$', get_videos_seen_for_person),
    (r'^savevideooffline/((?P<id>\d*)/)?$', save_video_offline),
    (r'^savevideofarmersonline/', save_personshowninvideo_online),
    (r'^getvideofarmersonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_personshowninvideo_online),
    (r'^savevideofarmersoffline/((?P<id>\d*)/)?$', save_personshowninvideo_offline),
    (r'^savedevelopmentmanageronline/((?P<id>\d*)/)?$', save_developmentmanager_online),
    (r'^getdevelopmentmanagersonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_developmentmanagers_online),
    (r'^savedevelopmentmanageroffline/((?P<id>\d*)/)?$', save_developmentmanager_offline),
    (r'^saveequipmentonline/((?P<id>\d*)/)?$', save_equipment_online),
    (r'^getequipmentsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_equipments_online),
    (r'^saveequipmentoffline/((?P<id>\d*)/)?$', save_equipment_offline),
    (r'^savedistrictonline/((?P<id>\d*)/)?$', save_district_online),
    (r'^getdistrictsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_districts_online),
    (r'^savedistrictoffline/((?P<id>\d*)/)?$', save_district_offline),
    (r'^saveblockonline/((?P<id>\d*)/)?$', save_block_online),
    (r'^getblocksonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_blocks_online),
    (r'^getblocksfordistrictonline/((?P<district_id>\d*)/)?$', get_blocks_for_district_online),
    (r'^saveblockoffline/((?P<id>\d*)/)?$', save_block_offline),
    (r'^savevillageonline/((?P<id>\d*)/)?$', save_village_online ),
    (r'^getvillagesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_villages_online),
    (r'^getvillagesforblocksonline/((?P<block_id>\d*)/)?$', get_villages_for_blocks_online),
    (r'^savevillageoffline/((?P<id>\d*)/)?$', save_village_offline),
    (r'^saveanimatoronline/((?P<id>\d*)/)?$', save_animator_online),
    (r'^getanimatorsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_animators_online),
    (r'^saveanimatoroffline/((?P<id>\d*)/)?$', save_animator_offline),
    (r'^saveanimatorassignedvillageonline/((?P<id>\d*)/)?$', save_animatorassignedvillage_online),
    (r'^getanimatorassignedvillagesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_animatorassignedvillages_online),
    (r'^saveanimatorassignedvillageoffline/((?P<id>\d*)/)?$', save_animatorassignedvillage_offline),
    (r'^savepersongrouponline/((?P<id>\d*)/)?$', save_persongroup_online),
    (r'^getpersongroupsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_persongroups_online),
    (r'^getpersongroupsforvillageonline/((?P<village_id>\d*)/)?$', get_persongroups_for_village_online),
    (r'^savepersongroupoffline/((?P<id>\d*)/)?$', save_persongroup_offline),
    (r'^savepersononline/((?P<id>\d*)/)?$', save_person_online),
    (r'^getpersonsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_persons_online),
    (r'^getpersonforvillageandnopersongrouponline/((?P<village_id>\d*)/)?$', get_person_for_village_and_no_person_group_online),
    (r'^getpersonforpersongrouponline/((?P<group_id>\d*)/)?$', get_person_for_person_group_online),
    (r'^savepersonoffline/((?P<id>\d*)/)?$', save_person_offline),
    (r'^savescreeningonline/((?P<id>\d*)/)?$', save_screening_online),
    (r'^getscreeningsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_screenings_online),
    (r'^savescreeningoffline/((?P<id>\d*)/)?$', save_screening_offline),
    (r'^getattendance/((?P<id>\d*)/)?$', get_attendance),
    (r'^getscreeningfarmergroupstargetedsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_groupstargetedinscreening_online),
    (r'^savescreeningfarmergroupstargetedsoffline/((?P<id>\d*)/)?$', save_groupstargetedinscreening_offline),
    (r'^savescreeningvideosscreenedsonline/$', save_videosscreenedinscreening_online),
    (r'^getscreeningvideosscreenedsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_videosscreenedinscreening_online),
    (r'^savescreeningvideosscreenedsoffline/((?P<id>\d*)/)?$', save_videosscreenedinscreening_offline),
    (r'^savetrainingonline/((?P<id>\d*)/)?$', save_training_online),
    (r'^gettrainingsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_trainings_online),
    (r'^savetrainingoffline/((?P<id>\d*)/)?$', save_training_offline),
    (r'^savetraininganimatorstrainedonline/?$', save_traininganimatorstrained_online),
    (r'^gettraininganimatorstrainedonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_traininganimatorstrained_online),
    (r'^savetraininganimatorstrainedoffline/((?P<id>\d*)/)?$', save_traininganimatorstrained_offline),
    (r'^savemonthlycostpervillageonline/$', save_monthlycostpervillage_online),
    (r'^getmonthlycostpervillagesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_monthlycostpervillages_online),
    (r'^savemonthlycostpervillageoffline/((?P<id>\d*)/)?$', save_monthlycostpervillage_offline),
    (r'^saveanimatorsalarypermonthonline/$', save_animatorsalarypermonth_online),
    (r'^getanimatorsalarypermonthsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_animatorsalarypermonths_online),
    (r'^saveanimatorsalarypermonthoffline/((?P<id>\d*)/)?$', save_animatorsalarypermonth_offline),
    (r'^savepersonrelationonline/$', save_personrelation_online),
    (r'^getpersonrelationsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_personrelations_online),
    (r'^savepersonrelationoffline/((?P<id>\d*)/)?$', save_personrelation_offline),
    (r'^getpersonmeetingattendancesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_personmeetingattendances_online),
    (r'^savepersonmeetingattendanceoffline/((?P<id>\d*)/)?$', save_personmeetingattendance_offline),
    (r'^savepersonadoptpracticeonline/((?P<id>\d*)/)?$', save_personadoptpractice_online),
    (r'^getpersonadoptpracticesonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_personadoptpractices_online),
    (r'^savepersonadoptpracticeoffline/((?P<id>\d*)/)?$', save_personadoptpractice_offline),
    (r'^saveequipmentholderonline/$', save_equipmentholder_online),
    (r'^getequipmentholdersonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_equipmentholders_online),
    (r'^saveequipmentholderoffline/((?P<id>\d*)/)?$', save_equipmentholder_offline),
    (r'^saverevieweronline/$', save_reviewer_online),
    (r'^getreviewersonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_reviewers_online),
    (r'^saverevieweroffline/((?P<id>\d*)/)?$', save_reviewer_offline),
    (r'^savetargetonline/((?P<id>\d*)/)?$', save_target_online),
    (r'^gettargetsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_targets_online),
    (r'^savetargetoffline/((?P<id>\d*)/)?$', save_target_offline),
    (r'^geterrorsonline/((?P<offset>\d*)/(?P<limit>\d*)/)?$', get_dashboard_errors_online),
    (r'^notanerror/((?P<offset>\d*)/(?P<limit>\d*)/)?$', mark_error_as_not_error),
    (r'^getindexdata/$', index_template_data),
    (r'^personsingroup/$',farmers_in_groups),
    (r'^personsinscreening/((?P<screening_id>\d*)/)?$', persons_in_screening),
    (r'^personmeetingattendance/(?P<person_id>\d*)/(?P<screening_id>\d*)', person_meeting_attendance_data),
    (r'^screeningsinvillage/((?P<village_id>\d*)/)?$', screenings_in_village),
    (r'^filtereddataforvillage/((?P<village_id>\d*)/)?$', filters_for_village),
    (r'^practicesforperson/((?P<person_id>\d*)/)?$', practices_seen_by_farmer),
    (r'^practicesinvideos/$', practices_in_videos),
)