from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
import logging
import pickle
from django.db.models import get_model, Max
import dashboard.models
#from social_website.models import Collection, ImageSpec, Milestone, Partner, Video
logger = logging.getLogger('social_website')


class ActivityType:
    facebook = 0
    new_collection = 1
    new_video = 2
    new_video_collection = 3
    new_village = 4
    video_milestone = 5
    village_milestone = 6
    screening_milestone = 7
    viewer_milestone = 8


def add_collection(collection):
    if len(collection.videos.all()) > 0:
        Activity = get_model('social_website','Activity')
        partner = collection.partner
        title = "%s shared a new collection" % (collection.partner.name).title()
        collection_name = (collection.title)
        video_number = len(collection.videos.all())
        state_name = collection.state
        country_name = (dashboard.models.State.objects.get(state_name=state_name)).country.country_name
        textContent = "Watch our new collection on %s with %s videos, produced in %s, %s." % (collection_name, video_number, state_name, country_name)
        date = collection.videos.aggregate(Max('date'))['date__max']
        newsFeed = 0
        titleURL = collection.get_absolute_url()
        activity_type = ActivityType.new_collection
        activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, collection_id=collection.uid, titleURL=titleURL, type=activity_type)
        activity.save()


def add_video(video):
    Activity = get_model('social_website','Activity')
    ImageSpec = get_model('social_website','ImageSpec')
    partner = video.partner
    title = "%s shared a new video" % (video.partner.name).title()
    video_title = (video.title).title()
    language_name = video.language
    village_name = (dashboard.models.Video.objects.get(id=video.coco_id)).village.village_name
    textContent = "Watch our new video on %s in %s. It has been created by community members of %s village." % (video_title, language_name, village_name)
    date = video.date
    newsFeed = 0
    imageURL = video.thumbnailURL16by9
    altString = "Video"
    imageLinkURL = "".join(["/video/?id=", str(video.coco_id)])
    titleURL = "".join(["/video/?id=", str(video.coco_id)])
    activity_type = ActivityType.new_video
    image_spec_entry = ImageSpec(imageURL=imageURL, altString=altString, imageLinkURL=imageLinkURL)
    image_spec_entry.save()
    activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, video_id = video.uid, titleURL=titleURL, type=activity_type)
    activity.save()
    activity.images.add(image_spec_entry)
    activity.save()


def add_video_collection(collection, video):
    Activity = get_model('social_website','Activity')
    print type(collection)
    partner = collection.partner
    title = collection.partner.name
    collection_name = (collection.title).title()
    video_title = (video.title).title()
    textContent = "We've added a new video to %s titled %s." % (collection_name, video_title)
    date = video.date
    newsFeed = 0
    titleURL = collection.get_absolute_url()
    activity_type = ActivityType.new_video_collection
    print type(Activity)
    activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, collection_id=collection.uid, video_id = video.uid, titleURL=titleURL, type=activity_type)
    activity.save()


def add_village(village, partner):
    file = "".join([dg.settings.MEDIA_ROOT, "village_partner_list.p"])
    village_partner_list = pickle.load(open(file, "rb"))
    Activity = get_model('social_website', 'Activity')
    screenings = dashboard.models.Screening.objects.exclude(videoes_screened__isnull = True).filter(village=village.id, user_created__cocouser__partner_id=partner.coco_id).order_by('date')
    if (len(screenings) > 0):
        title = partner.name
        date = screenings[0].date
        newsFeed = 0
        titleURL = partner.get_absolute_url()
        activity_type = ActivityType.new_village
        videos = screenings[0].videoes_screened.all()
        video_title = videos[0].title
        village_name = village.village_name
        textContent = "We just screened our first video, %s, in %s village." % (video_title, village_name)
        activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, titleURL=titleURL, type=activity_type)
        activity.save()
        village_partner_list.append((village.id, partner.uid))
    pickle.dump(village_partner_list, open(file, "wb"))


def add_milestone(partner):
    total_rows = 0
    Activity = get_model('social_website', 'Activity')
    ImageSpec = get_model('social_website', 'ImageSpec')
    Milestone = get_model('social_website', 'Milestone')
    Video = get_model('social_website', 'Video')
    milestone_video_village = [x * 10 for x in range(11)]
    milestone_video_village.extend([x * 25 for x in range(5, 9)])
    milestone_video_village.extend([x * 50 for x in range(5, 101)])

    milestone_screening_viewer = [0, 50]
    milestone_screening_viewer.extend([x * 100 for x in range(1, 3)])
    milestone_screening_viewer.extend([x * 500 for x in range(1, 5)])
    milestone_screening_viewer.extend([x * 1000 for x in range(3, 11)])
    milestone_screening_viewer.extend([x * 10000 for x in range(2, 11)])
    milestone_screening_viewer.extend([x * 25000 for x in range(5, 9)])
    milestone_screening_viewer.extend([x * 50000 for x in range(5, 101)])

    milestone = Milestone.objects.get(partner_id=partner.uid)
    videoNumber = milestone.videoNumber
    villageNumber = milestone.villageNumber
    screeningNumber = milestone.screeningNumber
    viewerNumber = milestone.viewerNumber

    # video milestone
    videos = Video.objects.filter(partner=partner).order_by('date')
    next_video_milestone = milestone_video_village[milestone_video_village.index(videoNumber) + 1]
    while (len(videos) >= next_video_milestone):
        video = videos[next_video_milestone - 1]
        partner = video.partner
        title = (video.partner.name).title() + " has produced %s+ videos" % (next_video_milestone)
        video_title = (video.title).title()
        language_name = video.language
        village_name = (dashboard.models.Video.objects.get(id=video.coco_id)).village.village_name
        textContent = "Watch our new video on %s in %s. It has been created by community members of %s village." % (video_title, language_name, village_name)
        date = video.date
        newsFeed = 0
        titleURL = "".join(["/video/?id=", str(video.coco_id)])
        activity_type = ActivityType.video_milestone
        imageURL = video.thumbnailURL16by9
        altString = "Video"
        imageLinkURL = "/video/?id=" + video.coco_id
        total_rows += 1
        image_spec_entry = ImageSpec(imageURL=imageURL, altString=altString, imageLinkURL=imageLinkURL)
        image_spec_entry.save()
        activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, video_id = video.uid, titleURL=titleURL, type=activity_type)
        activity.save()
        activity.images.add(image_spec_entry)
        activity.save()
        videoNumber = next_video_milestone
        milestone.videoNumber = videoNumber
        milestone.save()
        next_video_milestone = milestone_video_village[milestone_video_village.index(videoNumber) + 1]

    #village milestone
    villages = dashboard.models.Village.objects.exclude(start_date__isnull=True).filter(user_created__cocouser__partner_id=partner.coco_id).order_by('start_date')
    dashboard_partner_states = list(set(villages.values_list('block__district__state__state_name', flat=True)))
    next_village_milestone = milestone_video_village[milestone_video_village.index(villageNumber) + 1]
    while (len(villages) >= next_village_milestone):
        village = villages[next_village_milestone - 1]
        title = "%s is now sharing videos in %s+ villages." % ((partner.name).title(), next_village_milestone)
        if(len(dashboard_partner_states) > 1):
            states_name = ", ".join(dashboard_partner_states)
            textContent = "We have reached %s+ villages in the states of %s in partnership with Digital Green." % (next_village_milestone, states_name)
        else:
            textContent = "We have reached %s+ villages in the state of %s in partnership with Digital Green." % (next_village_milestone, dashboard_partner_states[0])
        date = village.start_date
        newsFeed = 0
        titleURL = partner.get_absolute_url()
        activity_type = ActivityType.village_milestone
        total_rows += 1
        activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, titleURL=titleURL, type=activity_type)
        activity.save()
        villageNumber = next_village_milestone
        milestone.villageNumber = villageNumber
        milestone.save()
        next_village_milestone = milestone_video_village[milestone_video_village.index(villageNumber) + 1]

    #screening milestone
    screenings = dashboard.models.Screening.objects.filter(user_created__cocouser__partner_id=partner.coco_id).order_by('date')
    next_screening_milestone = milestone_screening_viewer[milestone_screening_viewer.index(screeningNumber) + 1]
    while (len(screenings) >= next_screening_milestone):
        screening = screenings[next_screening_milestone - 1]
        title = (partner.name).title()
        textContent = "We just showed our %sth video in %s, %s since %s." % (next_screening_milestone,
                                                                                 screening.village.village_name,
                                                                                 screening.village.block.district.state.state_name,
                                                                                 screenings[0].date.strftime('%d %B %Y'))
        date = screening.date
        newsFeed = 0
        titleURL = partner.get_absolute_url()
        activity_type = ActivityType.screening_milestone
        total_rows += 1
        activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, titleURL=titleURL, type=activity_type)
        activity.save()
        screeningNumber = next_screening_milestone
        milestone.screeningNumber = screeningNumber
        milestone.save()
        next_screening_milestone = milestone_screening_viewer[milestone_screening_viewer.index(screeningNumber) + 1]

    #viwer milestone
    viewers = dashboard.models.PersonMeetingAttendance.objects.prefetch_related('screening').filter(screening__user_created__cocouser__partner_id=partner.coco_id).order_by('screening__date')
    next_viewer_milestone = milestone_screening_viewer[milestone_screening_viewer.index(viewerNumber) + 1]
    while (len(viewers) >= next_viewer_milestone):
        viewer = viewers[next_viewer_milestone - 1]
        title = (partner.name).title()
        textContent = "%s is our %sth viewer watching videos in %s" % ((viewer.person.person_name).title(),
                                                                          next_viewer_milestone,
                                                                          viewer.screening.village.block.district.state.state_name)
        date = viewer.screening.date
        newsFeed = 0
        titleURL = partner.get_absolute_url()
        activity_type = ActivityType.viewer_milestone
        total_rows += 1
        activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, titleURL=titleURL, type=activity_type)
        activity.save()
        viewerNumber = next_viewer_milestone
        milestone.viewerNumber = viewerNumber
        milestone.save()
        next_viewer_milestone = milestone_screening_viewer[milestone_screening_viewer.index(viewerNumber) + 1]
    logger.info("%s Rows To Be Added: %s" % (partner.name, total_rows))

if __name__ == '__main__':
    Activity = get_model('social_website', 'Activity')
    Collection = get_model('social_website', 'Collection')
    Milestone = get_model('social_website', 'Milestone')
    Partner = get_model('social_website', 'Partner')
    Video = get_model('social_website', 'Video')

    # Do this only if making afresh, NOT IN CRON !!
    Activity.objects.all().delete()
    Milestone.objects.all().delete()

    file_village = "".join([dg.settings.MEDIA_ROOT, "village_partner_list.p"])
    village_partner_list = []
    pickle.dump(village_partner_list, open(file_village, "wb"))
    file_collection = "".join([dg.settings.MEDIA_ROOT, "collection_dict.p"])
    collection_dict = {}
    for partner in Partner.objects.all():
        #Initial entry for milestone table
        milestone_object = Milestone(partner=partner, videoNumber=0, villageNumber=0, screeningNumber=0, viewerNumber=0)
        milestone_object.save()
        #Adding Village Added Activities for each partner
        for village in dashboard.models.Village.objects.exclude(start_date__isnull = True).order_by('-start_date')[:10]:
            add_village(village, partner)

        #Adding Collection Added Activities for each partner
        for collection in Collection.objects.filter(partner=partner):
            add_collection(collection)
            collection_dict[collection.uid] = []
            for video in collection.videos.all():
                collection_dict[collection.uid].append(video.uid)

        #Adding Video Added Activities for each partner
        for video in Video.objects.filter(partner=partner):
            add_video(video)
        #Adding Milestone Activities for each partner
        add_milestone(partner)
    pickle.dump(collection_dict, open(file_collection, "wb"))
