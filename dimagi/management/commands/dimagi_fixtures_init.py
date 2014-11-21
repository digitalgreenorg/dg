from datetime import datetime
from optparse import make_option
import json
import requests
from requests.auth import HTTPDigestAuth
from django.core.management.base import BaseCommand, CommandError
from dimagi.models import CommCareProject, CommCareUser
from dimagi.scripts.create_fixtures_functions import create_fixture, create_fixture_video
from dg.settings import DIMAGI_USERNAME, DIMAGI_PASSWORD


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-i', '--init',
                    action='store_true',
                    default=False,
                    help='First Time When Starting the Project'),
        make_option('-u', '--update',
                    action='store_true',
                    default=False,
                    help='Selective Update of Statistics'),
        )

    def handle(self, *args, **options):
        if (options['init']):
            self.generate(args, False)
        if (options['update']):
            self.generate(args, True)

    def generate(self, args, Update):
        commcare_project_list = args
        for commcare_project_name in commcare_project_list:
            try:
                commcare_project = CommCareProject.objects.get(name=commcare_project_name)
            except CommCareProject.DoesNotExist:
                raise CommandError('CommCare Project "%s" not yet entered in the Database.' % commcare_project_name)
            commcare_users = CommCareUser.objects.filter(project=commcare_project).all()

            # getting all the villages, groups, animators stored at commcare
            url_group = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", "?fixture_type=group"])
            url_village = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", "?fixture_type=village"])
            url_mediator = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", "?fixture_type=mediator"])

            list_group = []
            list_village = []
            list_mediator = []

            if Update:
                while(True):
                    r = requests.get(url_group, auth=HTTPDigestAuth(DIMAGI_USERNAME, DIMAGI_PASSWORD))
                    group_data = json.loads(r.content)
                    for obj in group_data['objects']:
                        list_group.append(str(obj['fields']['id']))
                    if(group_data['meta']['next']):
                        url_group = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", str(group_data['meta']['next'])])
                    else:
                        break
                print len(list_group)
                while(True):
                    r = requests.get(url_village, auth=HTTPDigestAuth(DIMAGI_USERNAME, DIMAGI_PASSWORD))
                    village_data = json.loads(r.content)
                    for obj in village_data['objects']:
                        list_village.append(str(obj['fields']['id']))
                    if(village_data['meta']['next']):
                        url_village = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", str(group_data['meta']['next'])])
                    else:
                        break
                print len(list_village)
                while(True):
                    r = requests.get(url_mediator, auth=HTTPDigestAuth(DIMAGI_USERNAME, DIMAGI_PASSWORD))
                    mediator_data = json.loads(r.content)
                    for obj in mediator_data['objects']:
                        list_mediator.append((str(obj['fields']['id']), str(obj['fields']['village_id'])))
                    if(mediator_data['meta']['next']):
                        url_mediator = "".join(["https://www.commcarehq.org/a/", commcare_project_name, "/api/v0.5/fixture/", str(group_data['meta']['next'])])
                    else:
                        break
                print len(list_mediator)
            create_fixture(commcare_users, commcare_project_name, list_group, list_village, list_mediator)
            # Run Video Fixtures on 5 Day of the Week
            if (datetime.utcnow().weekday() % 5) == 0 or not Update:
                create_fixture_video(commcare_project_name)
