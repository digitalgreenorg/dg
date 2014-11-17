import os

import json
import requests
from requests.auth import HTTPDigestAuth
from django.core.management.base import BaseCommand, CommandError
from dimagi.models import CommCareProject, CommCareUser
from dimagi.scripts.create_fixtures_functions import create_fixture, create_fixture_video


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
            # getting all the villages, groups, animators stored at commcare
            url_group = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", "?fixture_type=group"])
            url_village = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", "?fixture_type=village"])
            url_mediator = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", "?fixture_type=mediator"])

            list_group = []
            list_village = []
            list_mediator = []

            while(True):
                r = requests.get(url_group, auth=HTTPDigestAuth('nandinibhardwaj@gmail.com', 'digitalgreen'))
                group_data = json.loads(r.content)
                for obj in group_data['objects']:
                    list_group.append(str(obj['fields']['id']))
                if(group_data['meta']['next']):
                    url_group = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", str(group_data['meta']['next'])])
                else:
                    break
            print len(list_group)
            while(True):
                r = requests.get(url_village, auth=HTTPDigestAuth('nandinibhardwaj@gmail.com', 'digitalgreen'))
                village_data = json.loads(r.content)
                for obj in village_data['objects']:
                    list_village.append(str(obj['fields']['id']))
                if(village_data['meta']['next']):
                    url_village = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", str(group_data['meta']['next'])])
                else:
                    break
            print len(list_village)
            while(True):
                r = requests.get(url_mediator, auth=HTTPDigestAuth('nandinibhardwaj@gmail.com', 'digitalgreen'))
                mediator_data = json.loads(r.content)
                for obj in mediator_data['objects']:
                    list_mediator.append((str(obj['fields']['id']), str(obj['fields']['village_id'])))
                if(mediator_data['meta']['next']):
                    url_mediator = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", str(group_data['meta']['next'])])
                else:
                    break
            print len(list_mediator)
            create_fixture(commcare_users, commcare_project_name, list_group, list_village, list_mediator)
            create_fixture_video(commcare_project_name)
