import os
from django.core.management.base import BaseCommand, CommandError

from dg.settings import MEDIA_ROOT

from dimagi.models import CommCareProject, CommCareUser, CommCareUserVillage
from dimagi.scripts.userfile_functions import make_upload_file


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
            commcare_users = CommCareUser.objects.filter(project=commcare_project).all()
            for user in commcare_users:
                villages = CommCareUserVillage.objects.filter(user=user).values_list('village__id', flat =True)
                filename = os.path.join(MEDIA_ROOT, "dimagi", "%s.xml" % (user.username))
                file_to_upload = make_upload_file(
                    villages,
                    filename,
                    user.guid,
                    commcare_project.id
                )
                response = commcare_project.upload_case_file(filename)
                if response == 201 or response == 200:
                    self.stdout.write('Successfully uploaded cases for "%s"' % entry['username'])
                else:
                    self.stdout.write('Not uploaded but file ("%s") has been created in MEDIA_ROOT/dimagi' % entry['username'])
