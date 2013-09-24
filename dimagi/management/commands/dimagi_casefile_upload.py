from django.core.management.base import BaseCommand, CommandError
from dimagi.models import CommCareProject


class Command(BaseCommand):
    args = '<commcare_project_name> <commcare_project_name> ...'
    help = '''Pass the address of the file and project name'''
    
    def handle(self, *args, **options):
        filename = args[0]
        project = args[1]
        
        try:
            commcare_project = CommCareProject.objects.get(name=project)
        except CommCareProject.DoesNotExist:
            raise CommandError('CommCare Project "%s" not yet entered in the Database.' % commcare_project_name)
        
        try :
            response = commcare_project.upload_case_file(filename)
            if response.getcode() == 201 or response.getcode() == 200:
                self.stdout.write('Successfully uploaded cases \n')
        except Exception as ex:
            pass