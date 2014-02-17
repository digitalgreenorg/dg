import pickle

from django.db.models import get_model

import dg.settings

from social_website.utils.generate_activities import add_collection, add_video, add_video_collection


def increase_online_video_like(sender, **kwargs):
    instance = kwargs["instance"]
    try:
        video_to_update = get_model('social_website','Video').objects.get(uid = instance.video_id)
        video_to_update.onlineLikes += 1
        video_to_update.save()
        # update likes of all collections it belongs to 
        for collection in video_to_update.collection_set.all():
            collection.increase_likes()
        # update likes of the partner it belongs to
        video_to_update.partner.increase_likes()
    except Exception, ex:
        print ex


def video_add_activity(sender, **kwargs):
    instance = kwargs["instance"]
    if kwargs["created"]:
        video = get_model('social_website', 'Video').objects.get(uid=instance.uid)
        add_video(video)


def video_collection_activity(collection, videos):
    file = "".join([dg.settings.MEDIA_ROOT, "collection_dict.p"])
    collection_dict = pickle.load(open(file, "rb"))

    if collection.uid not in collection_dict:
        add_collection(collection)
        collection_dict[collection.uid]=[]

    for video_uid in videos:
        video = get_model('social_website', 'Video').objects.get(uid=video_uid)
        if video_uid not in collection_dict[collection.uid]:
            add_video_collection(collection, video)
            collection_dict[collection.uid].append(video.uid)
    pickle.dump(collection_dict, open(file, "wb"))
