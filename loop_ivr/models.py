from django.db import models
from loop.models import Crop, Mandi, LoopModel

INFO_STATUS = ((0, "Pending"), (1, "Done"), (2, "Wrong Query"), (3, "No Input"), (4, 'Not Picked'),(5,'Declined'))
RETURN_RESULT = ((0, "No"), (1, "Yes"))

class PriceInfoIncoming(LoopModel):
    id = models.AutoField(primary_key=True)
    call_id = models.CharField(max_length=100, db_index=True)
    from_number = models.CharField(max_length=20, db_index=True) #User No.
    to_number = models.CharField(max_length=20)                  #DG Exotel No.
    incoming_time = models.DateTimeField()
    info_status = models.IntegerField(choices=INFO_STATUS, default=4, db_index=True)
    query_code = models.CharField(max_length=120, null=True, blank=True)
    prev_info_status = models.IntegerField(choices=INFO_STATUS, default=4, db_index=True)
    prev_query_code = models.CharField(max_length=120, null=True, blank=True)
    price_result = models.TextField(null=True, blank=True)
    return_result_to_app = models.IntegerField(choices=RETURN_RESULT, default=1)

    def __unicode__(self):
        return "%s (%s)" % (self.from_number, self.incoming_time)

    class Meta:
        unique_together = ("call_id", "from_number", "incoming_time")


class PriceInfoLog(LoopModel):
    id = models.AutoField(primary_key=True)
    price_info_incoming = models.ForeignKey(PriceInfoIncoming)
    crop = models.ForeignKey(Crop)
    mandi = models.ForeignKey(Mandi)
