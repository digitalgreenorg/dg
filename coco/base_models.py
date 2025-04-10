from django.contrib.auth.models import User
from django.db import models

# Variables
TYPE_OF_ROLE = (
    (0, 'Animator'),
    (1, 'MRP'),
    (2, 'Video Producer')
)

ACTIVITY_CHOICES = (
    ('MKSP', 'MKSP'),
    ('LIVELIHOOD', 'LIVELIHOOD'),
    ('GOTARY', 'GOTARY'),
    ('HNN', 'HNN'),
)

DAY_CHOICES = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

VIDEO_TYPE = (
    (1, 'Eligible for Adoption'),
    (2, 'Not Eligible for adoption')
)

STORYBASE = (
    (1, 'Agricultural'),
    (2, 'Institutional'),
    (3, 'Health'),
)

ADOPTION_VERIFICATION = (
    (0, 'Not Checked'),
    (1, 'Approved'),
    (2, 'Rejected'),
)

SCREENING_OBSERVATION = (
    (0, 'Not Observed'),
    (1, 'Observed'),
)

SCREENING_GRADE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
)

VIDEO_REVIEW = (
    (0, 'Not Reviewed'),
    (1, 'Reviewed'),
)

VIDEO_GRADE = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)

VERIFIED_BY = (
    (0, 'Digital Green'),
    (1, 'Partner'),
    (2, 'Third Party'),
)

REVIEW_BY = (
    (0, 'Digital Green'),
    (1, 'Partner'),
)

NONNEGOTIABLE_OPTION = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

TYPE_OF_COCOUSER = (
    (1, 'HNN'),
    (2, 'AGRICULTURE'),
    (3, 'BOTH'),
    (4, 'UPAVAN'),
)

PARENT_CATEGORY = (
    (1, 'HNN'),
    (2, 'AGRICULTURE'),
)

ATTENDED_PERSON_CATEGORY = (
    (0, 'Pregnant Woman'),
    (1, 'Mother of a child up to 6 months'),
    (2, 'Mother of a child 6 months to 2 years'),
    (3, 'Mother of a child  2 to 5 years'),
    (4, 'Adolescent girl (10-19 years)'),
    (5, 'Woman of reproductive age (15-49 years)'),
)

ADOPT_PRACTICE_CATEGORY = (
    ("1", 'Yes'),
    ("2", 'No'),
    ("3", 'Not Applicable'),
)

FRONTLINE_WORKER_PRESENT = (
    ("1", 'ANM'),
    ("2", 'ASHA'),
    ("3", 'AWW'),
)

TYPE_OF_VENUE = (

    ('1', 'AWC'),
    ('2', 'school'),
    ('3', 'open space'),
    ('4', 'community hall'),
    ('5', 'other'),
)

TYPE_OF_VIDEO = (

    ('1', 'NSA video'),
    ('2', 'MIYCN video'),
    ('3', 'PLA video'),
    ('4', 'PLA meeting'),
)

TOPICS = (

    ('1', 'Introduction and understanding social inequities'),
    ('2', 'Understanding underlying causes of under nutrition'),
    ('3', 'Identifying problems that affect nutrition conditions during the 1000-day'),
    ('4', 'Prioritizing problems'),
    ('5', 'Understanding the causes and effects'),
    ('6', 'Understanding barriers and opportunities'),
    ('7', 'Accountability and sharing of Responsibilities'),
    ('8', 'Planning and sharing of responsibilities for Village interface Meeting')
)

# Choice tuples for Farmer Feedback
VIDEO_RELEVANCE_CHOICES = (
    ('relevant', 'Relevant to a great extent'),
    ('relevant_to_som_extnt', 'Relevant to some extent'),
    ('not_relevant', 'Not Relevant'),
)

YES_NO_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
)

NON_ADOPTION_REASON_CHOICES = (
    ('a', "Since I am not clear and convinced in the importance of the technology"),
    ('b', "The input/technology/service for the recommended practice is not easily accessible"),
    ('c', "The cost of the recommended practice is not affordable, and there is no credit facility in our kebele"),
    ('d', "The risk of the investment in the recommended practice is not acceptable"),
    ('e', "Unavailability of Inputs at the Market"),
    ('f', "The technology needs human power and I don't have that"),
    ('g', "The time has passed to adopt the technology"),
    ('h', "My spouse is the one who makes the decision"),
    ('i', "The DA/Mediator will not provide support after dissemination"),
    ('j', "Other (Please specify)")
)

LOCATION_CONVENIENCE_CHOICES = (
    ('safe', 'Safe and convenient'),
    ('too_far', 'Too far from my house'),
    ('isolated', 'Isolated / not safe to come alone'),
    ('other', 'Other'),
)

TIME_CONVENIENCE_CHOICES = (
    ('early_morning', 'Early in the Morning'),
    ('mid_day', 'Mid Day'),
    ('afternoon', 'In the Afternoon'),
    ('late_afternoon', 'Late in the Afternoon'),
    ('evening', 'In the Evening'),
)

DISSEMINATION_CHALLENGES_CHOICES = (
    ('a', "My husband is not willing to send me for such events"),
    ('b', "Busy with household chores and social/family issues"),
    ('c', "Mostly the dissemination schedules have been organized in Market days"),
    ('d', "I don't have information about the dissemination schedules"),
    ('e', "Have no one to take care of my children"),
    ('f', "Other (Please specify)")
)

PARTICIPATION_DISCOMFORT_REASONS_CHOICES = (
    ('a', "The DA/Mediator was not encouraging to ask questions"),
    ('b', "The DA/Mediator was only focusing on Model Farmers"),
    ('c', "The DA/Mediator was not encouraging Female Farmers"),
    ('d', "I feel comfortable with Female only group (Female farmers)"),
    ('e', "I am not clear with the topic"),
    ('f', "The topic is not relevant for me"),
    ('g', "The topic is not seasonal"),
    ('h', "I don't have the listed resources to adopt the technology"),
    ('i', "There is not enough time allocated for discussion"),
    ('j', "Other (Please specify)")
)

NNG_RECALL_CHOICES = (
    ('all', 'Recalled all NNGs'),
    ('partial', 'Recalled partially'),
    ('none', 'Did not recall'),
)


class CocoModel(models.Model):
    user_created = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_created", editable=False, null=True, blank=True)
    time_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    user_modified = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_related_modified", editable=False, null=True, blank=True)
    time_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
