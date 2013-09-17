import os
import shutil
from django.core.management.base import BaseCommand, CommandError

from dg.settings import MEDIA_ROOT

from dimagi.models import CommCareProject, CommCareUser, CommCareUserVillage


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
            
            
            # Save your last update timestamp.
            
            # Get a list of all villages in all projects 
            # Make a call to serverlog. Get new Person or PMA ids and actions since timestamp, filtering on villages
            # 1. new persons added => create a new case
            # 2. person edited => update all case properties
            # 3. person delete => close case
            # 4. pma add => update case with video seen
            # 5. pma edit => 
            # list2 = persons edited
            deleted 
            # list2 = new oma
            
            
            
            #TODO Change to MEDIA_ROOT etcetera
            scripts_dir = os.path.dirname(__file__)
            dir = scripts_dir + "\case_update"
            completed_dir = scripts_dir + "\uploaded"
            if not os.path.exists(completed_dir):
                os.makedirs(completed_dir)
            files = os.listdir(dir)
            uploaded = []
            for file in files:
                filename = os.path.join(dir,file)
                try : 
                    response = commcare_project.upload_case_file(filename)
                    if response == 201 or response == 200:
                        uploaded.append(filename)
                        shutil.move(filename, completed_dir)
                except Exception as ex:
                    pass
    