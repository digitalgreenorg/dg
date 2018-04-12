import json
import requests
from requests.auth import HTTPDigestAuth

from dg.settings import DIMAGI_USERNAME, DIMAGI_PASSWORD


def create_dimagi_user(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.pk is None:
        instance.username = instance.coco_user.user.username
        url = "".join(["https://www.commcarehq.org/a/", str(instance.project.name), "/api/v0.5/user/"])
        payload = {"username": "".join([instance.coco_user.user.username, '@', str(instance.project.name), '.commcarehq.org']),
                   "password": "123",
                   "groups": [str(instance.project.group_id)]
                   }
        r = requests.post(url, data=json.dumps(payload), auth=HTTPDigestAuth(DIMAGI_USERNAME, DIMAGI_PASSWORD))
        content = json.loads(r.content)
        instance.guid = str(content['id'])
