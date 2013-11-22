import os

from django.core.management.base import BaseCommand, CommandError
from dimagi.models import CommCareProject, CommCareUser
from dimagi.scripts.create_fixtures_functions import create_fixture


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

            #The following function creates an excel workbook with project_name
            want_seasonal_behavior = "yes" 
            create_fixture(commcare_users, commcare_project_name, want_seasonal_behavior)
