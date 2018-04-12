from django.db import models


class FarmerbookManager(models.Manager):
    def get_query_set(self):
        return super(FarmerbookManager, self).get_query_set().filter(image_exists=True)

class VillageFarmerbookManager(models.Manager):
    def get_query_set(self):
        return super(VillageFarmerbookManager, self).get_query_set().filter(person__image_exists=True).distinct()
