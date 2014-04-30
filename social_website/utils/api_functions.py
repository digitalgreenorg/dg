from social_website.models import VideoinCollection


def add_video_collection(collection_id, video_list):
    existing_video_list = set(VideoinCollection.objects.filter(collection_id=collection_id).values_list('video_id', flat=True))
    for index, video in enumerate(video_list):
            try:
                vid_collection = VideoinCollection.objects.get(collection_id=collection_id, video_id=video)
                vid_collection.order = index
            except VideoinCollection.DoesNotExist:
                vid_collection = VideoinCollection(collection_id=collection_id, video_id=video, order=index)
            finally:
                vid_collection.save()
    video_list = [int(i) for i in video_list]
    delete_video_set = existing_video_list - set(video_list)
    VideoinCollection.objects.filter(collection_id=collection_id, video_id__in=delete_video_set).delete()