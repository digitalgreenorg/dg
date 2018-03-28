from django.db import models
from loop.models import Crop, Mandi, LoopModel

INFO_STATUS = ((0, "Pending"), (1, "Done"), (2, "Wrong Query"), (3, "No Input"), (4, 'Not Picked/Declined'), (5, 'Call Not Initiated'))
RETURN_RESULT = ((0, "No"), (1, "Yes"))
TYPE_OF_SUBSCRIBER = ((0, "Farmer"), (1, "Aggregator"), (2, "DG"), (3, "Other"))
STATUS = ((0, "Inactive"), (1, "Active"))
SMS_STATUS = ((0, "Pending"), (1, "Sent"), (2, "Failed"), (3, "Failed-DND"))
CALL_SOURCE = ((1, "Exotel Call"), (2, "Textlocal Call"), (3, "Textlocal SMS"))

class PriceInfoIncoming(LoopModel):
    id = models.AutoField(primary_key=True)
    call_id = models.CharField(verbose_name="Call / Message Id", max_length=100, db_index=True)
    from_number = models.CharField(max_length=20, db_index=True) #User No.
    to_number = models.CharField(max_length=20)                  #DG Exotel No.
    incoming_time = models.DateTimeField()
    info_status = models.IntegerField(choices=INFO_STATUS, default=4, db_index=True)
    query_code = models.CharField(max_length=120, null=True, blank=True)
    prev_info_status = models.IntegerField(choices=INFO_STATUS, default=4, db_index=True)
    prev_query_code = models.CharField(max_length=120, null=True, blank=True)
    price_result = models.TextField(null=True, blank=True)
    return_result_to_app = models.IntegerField(choices=RETURN_RESULT, default=1)
    call_source = models.IntegerField(choices=CALL_SOURCE, default=1)
    textlocal_sms_id = models.TextField(null=True, blank=True)  #Comma Seprated Multiple SMS id
    server_response_time = models.DateTimeField(verbose_name="Time at which server makes API call to textlocal", blank=True, null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.from_number, self.incoming_time)

    class Meta:
        unique_together = ("call_id", "from_number", "incoming_time")


class PriceInfoLog(LoopModel):
    id = models.AutoField(primary_key=True)
    price_info_incoming = models.ForeignKey(PriceInfoIncoming)
    crop = models.ForeignKey(Crop)
    mandi = models.ForeignKey(Mandi)


class Subscriber(LoopModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone_no = models.CharField(max_length=14, unique=True)
    type_of_subscriber = models.IntegerField(choices=TYPE_OF_SUBSCRIBER, default=3)
    status = models.IntegerField(choices=STATUS, default=1)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.phone_no)


class Subscription(LoopModel):
    id = models.AutoField(primary_key=True)
    subscriber = models.ForeignKey(Subscriber)
    start_date = models.DateTimeField()
    subscription_code = models.CharField(max_length=150)
    status = models.IntegerField(choices=STATUS, default=1)

    def __unicode__(self):
        return "%s (%s)" % (self.subscriber, self.subscription_code)

    class Meta:
        unique_together = ("subscriber", "subscription_code")


class SubscriptionLog(LoopModel):
    id = models.AutoField(primary_key=True)
    subscription = models.ForeignKey(Subscription)
    date = models.DateTimeField()
    sms_id = models.CharField(max_length=150, null=True, blank=True)
    status = models.IntegerField(choices=SMS_STATUS, default=0)

    def __unicode__(self):
        return "%s (%s)" % (self.subscription, self.status)
