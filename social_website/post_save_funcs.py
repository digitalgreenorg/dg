from django.db.models import get_model

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
        
def collection_video_save(sender, **kwargs):
    if kwargs['action'] == 'post_add':
        print "here"
        from migration_functions import populate_collection_stats, populate_partner_stats
        collection = kwargs["instance"]
        populate_collection_stats(collection)
        populate_partner_stats(collection.partner)
        collection.save()
        collection.partner.save()
    
    