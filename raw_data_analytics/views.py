__author__ = 'HP'
import json, datetime
import numpy as np
import pandas as pd
import mysql

from django.http import HttpResponse

from activities.models import *
from programs.models import *
from geographies.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext


