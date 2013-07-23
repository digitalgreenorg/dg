from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)

from django.db.models import get_model

import dashboard.models
from social_website.models import Activity, ImageSpec, Milestone, Partner, Video


def add_collection(collection):
    partner = collection.partner
    title = (collection.partner.name).title() + " shared a new collection"
    collection_name = (collection.title)
    video_number = len(collection.videos.all())
    state_name = collection.state
    dashboard_state = get_model('dashboard', 'State')
    country_name = (dashboard_state.objects.get(state_name=state_name)).country.country_name
    textContent = "Watch our new collection on %s with %s videos, produced in %s, %s." % (collection_name, video_number, state_name, country_name)
    date = (max((collection.videos.values('date'))))['date']
    newsFeed = 0
    titleURL = "".join(["/social/collections/?id=", str(collection.uid), "&video=1"])
    activity_type = '1'
    activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, collection_id=collection.uid, titleURL=titleURL, type=activity_type)
    activity.save()


def add_video(video):
    partner = video.partner
    title = (video.partner.name).title() + " shared a new video"
    video_title = (video.title).title()
    language_name = video.language
    dashboard_video = get_model('dashboard', 'Video')
    village_name = (dashboard_video.objects.get(id=video.coco_id)).village.village_name
    textContent = "Watch our new video on %s in %s. It has been created by community members of %s village." % (video_title, language_name, village_name)
    date = video.date
    newsFeed = 0
    imageURL = video.thumbnailURL16by9
    altString = "Video"
    imageLinkURL = "/video/?id=" + video.coco_id
    titleURL = "".join(["/video/?id=", str(video.coco_id)])
    activity_type = '2'

    image_spec_entry = ImageSpec(imageURL=imageURL, altString=altString, imageLinkURL=imageLinkURL)
    image_spec_entry.save()
    activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, video_id = video.uid, titleURL=titleURL, type=activity_type)
    activity.save()
    activity.images.add(image_spec_entry)
    activity.save()


def add_video_collection(video_collection):
    collection = video_collection.collection
    video = video_collection.video
    partner = video.partner
    title = collection.partner.name
    collection_name = (collection.title).title()
    video_title = (video.title).title()
    textContent = "We've added a new video to %s titled %s." % (collection_name, video_title)
    date = video.date
    newsFeed = 0
    titleURL = "".join(["/social/collections/?id=", str(collection.uid), "&video=1"])
    activity_type = '3'
    activity = Activity(partner_id=partner.uid, title=title, textContent=textContent, date=date, newsFeed=newsFeed, collection_id=collection.uid, video_id = video.id, titleURL=titleURL, type=activity_type)
    activity.save()


def add_village(village):
    dashboard_screening = get_model('dashboard', 'Screening')
    screenings = dashboard_screening.objects.filter(village=village.id).order_by('date')
    if (len(screenings) > 0):
        partner = Partner.objects.get(coco_id=village.block.district.partner.id)
        title = partner.name
        date = screenings[0].date
        newsFeed = 0
        titleURL = ''
        activity_type = '4'
        videos = screenings[0].videoes_screened.all()
        video_title = videos[0].title
        village_name = village.village_name
        textContent = "We just screened our first video, %s, in %s village." % (video_title, village_name)
        activity = Activity(partner=partner, title=title, textContent=textContent, date=date, newsFeed=newsFeed, titleURL=titleURL, type=activity_type)
        activity.save()


def add_milestone(partner):
    print partner
    print type(partner)
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
    dashboard_video = get_model('dashboard', 'Video')
    while True:
        index = milestone_video_village.index(int(videoNumber)) + 1
        next_video_milestone = int(milestone_video_village[index])
        print next_video_milestone
        if(len(videos) >= next_video_milestone):
            video = videos[next_video_milestone]
            partner = video.partner
            title = (video.partner.name).title() + " has produced %s+ videos" % (next_video_milestone)
            video_title = (video.title).title()
            language_name = video.language
            village_name = (dashboard_video.objects.get(id=video.coco_id)).village.village_name
            textContent = "Watch our new video on %s in %s. It has been created by community members of %s village." % (video_title, language_name, village_name)
            date = video.date
            newsFeed = 0
            titleURL = "".join(["/video/?id=", str(video.coco_id)])
            activity_type = '5'
            imageURL = video.thumbnailURL16by9
            altString = "Video"
            imageLinkURL = "/video/?id=" + video.coco_id
            image_spec_entry = ImageSpec(imageURL=imageURL, altString=altString, imageLinkURL=imageLinkURL)
            image_spec_entry.save()
            activity = Activity(partner=partner, title=title, textContent=textContent, date=date, newsFeed=newsFeed, video = video, titleURL=titleURL, type=activity_type)
            activity.save()
            activity.images.add(image_spec_entry)
            activity.save()
            videoNumber = next_video_milestone
            milestone.videoNumber = videoNumber
            milestone.save()
        else:
            break

    #village milestone
    dashboard_village = get_model('dashboard', 'Village')
    dashboard_partner = get_model('dashboard', 'Partners')
    villages = dashboard_village.objects.exclude(start_date__isnull=True).filter(block__district__partner__id = partner.coco_id).order_by('start_date')
    while True:
       index =  milestone_video_village.index(int(villageNumber)) + 1
       next_village_milestone = int(milestone_video_village[index])
       dashboard_partner_obj = dashboard_partner.objects.get(id = partner.coco_id)
       dashboard_partner_states = dashboard_partner_obj.district_set.values_list('state__state_name', flat=True).distinct()
       if(len(villages) >= next_village_milestone):
           village = villages[next_village_milestone]
           partner_obj = partner
           title = "%s is now sharing videos in %s+ villages." % ((partner.name).title(), next_village_milestone)
           if(len(dashboard_partner_states) > 1):
                states_name = ", ".join(dashboard_partner_states)
                textContent = "We have reached %s+ villages in the states of %s in partnership with Digital Green." % (next_village_milestone, states_name)
           else:
                textContent = "We have reached %s+ villages in the state of %s in partnership with Digital Green." % (next_village_milestone, dashboard_partner_states[0])
           date = village.start_date
           newsFeed = 0
           titleURL = ""
           activity_type = '6'
           activity = Activity(partner=partner, title=title, textContent=textContent, date=date, newsFeed=newsFeed, titleURL=titleURL, type=activity_type)
           activity.save()
           villageNumber = next_village_milestone
           milestone.villageNumber = villageNumber
           milestone.save()
       else:
           break

    #screening milestone
    dashboard_screening = get_model('dashboard', 'Screening')
    screenings = dashboard_screening.objects.filter(village__block__district__partner__id=partner.coco_id).order_by('date')
    while True:
        index = milestone_screening_viewer.index(int(screeningNumber)) + 1
        next_screening_milestone = int(milestone_screening_viewer[index])
        print next_screening_milestone
        if(len(screenings) >= next_screening_milestone):
           screening = screenings[next_screening_milestone]
           title = (partner.name).title()
           textContent = "We just showed our %sth video in %s, %s since %s." % (next_screening_milestone,
                                                                                screening.village.village_name,
                                                                                screening.village.block.district.state.state_name,
                                                                                screenings[0].date.strftime('%d %B %Y'))
           date = screening.date
           newsFeed = 0
           titleURL = ""
           activity_type = '7'
           activity = Activity(partner=partner, title=title, textContent=textContent, date=date, newsFeed=newsFeed, titleURL=titleURL, type=activity_type)
           activity.save()
           screeningNumber = next_screening_milestone
           milestone.screeningNumber = screeningNumber
           milestone.save()
        else:
           break

    #viwer milestone
    dashboard_pma = get_model('dashboard', 'PersonMeetingAttendance')
    viewers = dashboard_pma.objects.prefetch_related('screening').filter(screening__village__block__district__partner__id = partner.coco_id).order_by('screening__date')
    while True:
        index = milestone_screening_viewer.index(int(viewerNumber)) + 1
        next_viewer_milestone = int(milestone_screening_viewer[index])
        if(len(viewers) >= next_viewer_milestone):
           viewer = viewers[next_viewer_milestone]
           title = (partner.name).title()
           textContent = "%s is our %sth viewer watching videos in %s" % ((viewer.person.person_name).title(),
                                                                          next_viewer_milestone,
                                                                          viewer.screening.village.block.district.state.state_name)
           date = viewer.screening.date
           newsFeed = 0
           titleURL = ""
           activity_type = '8'
           activity = Activity(partner=partner, title=title, textContent=textContent, date=date, newsFeed=newsFeed, titleURL=titleURL, type=activity_type)
           activity.save()
           viewerNumber = next_viewer_milestone
           milestone.viewerNumber = viewerNumber
        else:
           break
