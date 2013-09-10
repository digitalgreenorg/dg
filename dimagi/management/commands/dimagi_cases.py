import os

from django.core.management.base import BaseCommand, CommandError
from dg.settings import MEDIA_ROOT

from dimagi.models import CommCareProject, CommCareUser
from diamgi.userfile_functions import read_userfile, make_upload_file, upload_file


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
            commcare_users = CommCareUsers.objects.filter(project=commcare_project).all()
            for user in commcare_users:
                villages = [village.id for village in user.villages]
                filename = os.path.join(MEDIA_ROOT, "dimagi", "%s.xml" % (user.username))
                case_user_dict = {}
                case_person_dict = {}
                file_to_upload = make_upload_file(
                    villages,
                    filename,
                    user.guid,
                    case_user_dict,
                    case_person_dict
                )
                response = commcare_project.upload_case_file(filename)
                if response == 201 or response == 200:
                    self.stdout.write('Successfully closed poll "%s"' % poll_id) "" +entry['username']
