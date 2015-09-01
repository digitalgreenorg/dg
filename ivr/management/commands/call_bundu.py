import os
from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

from jharkhand_pilot import JharkhandPilot

class Command(BaseCommand):
    def handle(self, *args, **options):
    number = [7739889283,9905067616,8102831982,8252430499,7739324839,9006175257,7677121036,9523034070,9905128958,8434144393,7070384302,7677266209,9608316038,9608906302,9334602176,9546221064,7759886520,9905713048,9162753561,8102802186,9631756132,9308967196,7050590495]
    service = JharkhandPilot()
    for n in number:
        service.init_call(n)
