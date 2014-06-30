import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model
from datetime import datetime, timedelta
from dg.settings import MEDIA_ROOT

from dimagi.models import CommCareProject, CommCareUser, CommCareCase
from dimagi.scripts.update_cases_functions import close_case, update_case, write_new_cases
from people.models import Person


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
            case_new_list = []
            case_update_list = []
            for user in CommCareUser.objects.filter(project=commcare_project):
                print user
                for village in user.assigned_villages.all():
                    for person in Person.objects.filter(village=village):
                        try:
                            case = CommCareCase.objects.get(person=person, user=user, project=commcare_project, is_open=True)
                            case_update_list.append(case)
                        except CommCareCase.DoesNotExist:
                            case_new_list.append({'person': person, 'user': user})

            #===================================================================
            # Close Case will be handles later
            # Algorithm
            # Go through all the open cases
            # If the person exist don't do anything
            # If that person doesn't exist close the case
            #===================================================================

            if len(case_new_list):
                # Write XML for Creating Cases into file
                print 'creating new cases'
                filename_newcases = os.path.join(MEDIA_ROOT, "dimagi", "updates", "%s_newcase.xml" % (commcare_project_name))
                write_new_cases(case_new_list, filename_newcases, commcare_project)

                try:
                    response_new = commcare_project.upload_case_file(filename_newcases)
                    if response_new == 201 or response_new == 200:
                        self.stdout.write('Successfully created new cases for "%s"' % commcare_project_name)
                    else:
                        self.stdout.write('Not uploaded but file ("%s") has been created in MEDIA_ROOT/dimagi/updates' % commcare_project_name)
                except Exception as ex:
                    pass

            #===================================================================
            # if len(case_close_set):
            #     # Write XML for Closing Cases into file
            #     file_closecase = os.path.join(MEDIA_ROOT, "dimagi", "updates", "%s_closecase.xml" % (commcare_project_name))
            #     close_case(case_close_set, file_closecase)
            #     try:
            #         response_closecase = commcare_project.upload_case_file(file_closecase)
            #         if response_closecase == 201 or response_closecase == 200:
            #             self.stdout.write('Successfully closed case for "%s"' % commcare_project_name)
            #         else:
            #             self.stdout.write('Not closed but file ("%s") has been created in MEDIA_ROOT/dimagi/updates' % commcare_project_name)
            #     except Exception as ex:
            #         pass
            #===================================================================

            if len(case_update_list):
                filename_updatecases = os.path.join(MEDIA_ROOT, "dimagi", "updates", "%s_updatecase.xml" % (commcare_project_name))
                update_case(case_update_list, filename_updatecases)
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
