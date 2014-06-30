import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model
from datetime import datetime, timedelta
from dg.settings import MEDIA_ROOT

from dimagi.models import CommCareProject, CommCareUser, CommCareCase
from dimagi.scripts.update_cases_functions import close_case, update_case, write_new_case


class Command(BaseCommand):
    args = '<commcare_project_name> <commcare_project_name> ...'
    help = '''Creates initial cases for a new CommCare Application. Prerequisites:
    (1) Create project in CommCare.
    (2) Enter project information through admin.
    (3) Create atleast one CommCare user for this project.
    (4) Enter user, project and village permissions, through admin.
    '''

    def handle(self, *args, **options):
        commcare_project_list = args
        for commcare_project_name in commcare_project_list:
            try:
                commcare_project = CommCareProject.objects.get(name=commcare_project_name)
            except CommCareProject.DoesNotExist:
                raise CommandError('CommCare Project "%s" not yet entered in the Database.' % commcare_project_name)

            last_update_time = datetime.now() - timedelta(days=1)
            villages = CommCareUser.objects.filter(project=commcare_project.id).values_list('assigned_villages', flat=True)
            ServerLog = get_model('dashboard','ServerLog')

            persons_list = ServerLog.objects.filter(entry_table='Person').filter(village__in=villages).filter(timestamp__gte=last_update_time)

            person_new_set = set()
            person_update_set = set()
            person_close_set = set()

            case_update_set = set()
            case_close_set = set()

            for person in persons_list:
                if person.action == -1:
                    cases = CommCareCase.objects.filter(person_id=person.model_id, project=commcare_project, is_open=True)
                    person_close_set.add(person.model_id)
                    if len(cases):
                        for case in cases:
                            case_close_set.add(case)
                            case.is_open = False
                            case.save()
                elif person.action == 0:
                    person_update_set.add(person.model_id)
                else:
                    person_new_set.add(person.model_id)
            # If the case has been closed, there is no need to create or update it. If a case, does not exist, the assumption is that closing will proceed without error.
            person_new_set = person_new_set - person_close_set
            person_update_set = person_update_set - person_new_set - person_close_set

            for person_id in person_update_set:
                cases = CommCareCase.objects.filter(person_id=person_id, project=commcare_project, is_open=True)
                if len(cases):
                    for case in cases:
                        case_update_set.add(case)

            if len(person_new_set):
                # Write XML for Creating Cases into file
                filename_newcases = os.path.join(MEDIA_ROOT, "dimagi", "updates", "%s_newcase.xml" % (commcare_project_name))
                write_new_case(person_new_set, filename_newcases)

                try:
                    response_new = commcare_project.upload_case_file(filename_newcases)
                    if response_new == 201 or response_new == 200:
                        self.stdout.write('Successfully created new cases for "%s"' % commcare_project_name)
                    else:
                        self.stdout.write('Not uploaded but file ("%s") has been created in MEDIA_ROOT/dimagi/updates' % commcare_project_name)
                except Exception as ex:
                    pass

            if len(case_close_set):
                # Write XML for Closing Cases into file
                file_closecase = os.path.join(MEDIA_ROOT, "dimagi", "updates", "%s_closecase.xml" % (commcare_project_name))
                close_case(case_close_set, file_closecase)
                try:
                    response_closecase = commcare_project.upload_case_file(file_closecase)
                    if response_closecase == 201 or response_closecase == 200:
                        self.stdout.write('Successfully closed case for "%s"' % commcare_project_name)
                    else:
                        self.stdout.write('Not closed but file ("%s") has been created in MEDIA_ROOT/dimagi/updates' % commcare_project_name)
                except Exception as ex:
                    pass

            if len(case_update_set):
                filename_updatecases = os.path.join(MEDIA_ROOT, "dimagi", "updates", "%s_updatecase.xml" % (commcare_project_name))
                update_case(case_update_set, filename_updatecases)
                try:
                    response_update = commcare_project.upload_case_file(filename_updatecases)
                    if response_update == 201 or response_update == 200:
                        self.stdout.write('Successfully updated cases for "%s" \n' % commcare_project_name)
                    else:
                        self.stdout.write('HTTP response code: %d. Not uploaded but file ("%s") has been created in MEDIA_ROOT/dimagi/updates' % (commcare_project_name))
                except Exception as ex:
                    pass

        commcare_project.last_updated_time = datetime.now()
        commcare_project.save()
