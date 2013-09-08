import urllib2

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<commcare_project_name> <commcare_project_name> ...'
    help = ''' Deletes fixtures for stated CommCare Project.
    
    Prerequisites:
    (1) Create project in CommCare.
    (2) Enter project information through admin.
    (3) Create atleast one CommCare user for this project.
    (4) Enter user, project and village permissions, through admin.
    '''

    def handle(self, *args, **options):
        for commcare_project_name in commcare_project_list:
            try:
                commcare_project = CommCareProject.objects.get(name=commcare_project_name)
            except CommCareProject.DoesNotExist:
                raise CommandError('CommCare Project "%s" not yet entered in the Database.' % commcare_project_name)
            
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            opener.addheaders =[('User-agent', 'Mozilla/5.0'),
                                 ('user', 'nandini@digitalgreen:digitalgreen'),
                                 ('Cookie', 'csrftoken=97a5a243ad2abf742d6efb8c8d761c4f; sessionid=2b175aad09329500ba61126ecc88cf20; __utma=166502700.872983835.1346667629.1354086932.1354120837.88; __utmb=166502700.3.10.1354120837; __utmc=166502700; __utmz=166502700.1352897150.78.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)')]
            response = opener.open(project.fixture_url)
            # Data Types Retrieved
            string_response = response.read() 
            types = string_response.split('fields')
            ids_to_delete = []
            for i in range(len(types)-1):
                ids_to_delete.append(types[i+1].partition('_id": "')[2].partition('"}')[0])
            print ids_to_delete
            if len(ids_to_delete) == 0:
                print "Nothing to delete"
            else:
                for id in ids_to_delete:
                    try:
                        request_string = 'https://www.commcarehq.org/a/digitalgreen/fixtures/data-types/' + str(id)
                        request = urllib2.Request(request_string)
                        request.get_method = lambda: 'DELETE'
                        url = opener.open(request)
                        print "Deleted item : " + str(id)
                    except Exception as ex:
                        print " Could not delete item : " + str (id)
        