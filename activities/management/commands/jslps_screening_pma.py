import urllib2
from datetime import * 
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from geographies.models import *
from people.models import *
from programs.models import *
from videos.models import *
from activities.models import *