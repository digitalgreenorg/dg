import json
import requests
from requests.auth import HTTPDigestAuth


def create_dimagi_user(sender, **kwargs):
    instance = kwargs["instance"]
    print instance
    if instance.pk is None:
        instance.username = instance.coco_user.user.username
        url = "".join(["https://www.commcarehq.org/a/", str(instance.project.name), "/api/v0.5/user/"])
        payload = {"username" : instance.coco_user.user.username,
                   "password" : "123",
                   "groups": ["b0bba9ba517f83baf88d090e8b620753"]
                   }
        r = requests.post(url, data=json.dumps(payload), auth=HTTPDigestAuth('nandinibhardwaj@gmail.com', 'digitalgreen'))
        content = json.loads(r.content)
        print content
        instance.guid = str(content['id'])
