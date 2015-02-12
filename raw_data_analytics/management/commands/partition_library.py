__author__ = 'Lokesh'
import os.path
from optparse import make_option
import csv

from django.core.management.base import BaseCommand

from raw_data_analytics.utils.data_library import data_lib
import dg.settings


class Command(BaseCommand):
    # --- defining options for the command line exceution of the library ---
    option_list = BaseCommand.option_list + (
        make_option('-p', '--partner',
                    action='store',
                    default=False,
                    dest='partner',
                    help='Takes partner name as input for filter'),
        make_option('-c', '--country',
                    action='store',
                    default=False,
                    dest='country',
                    help='Takes country name as input for filter'),
        make_option('-s', '--state',
                    action='store',
                    default=False,
                    dest='state',
                    help='Takes state name as input for filter'),
        make_option('-d', '--district',
                    action='store',
                    default=False,
                    dest='district',
                    help='Takes district name as input for filter'),
        make_option('-b', '--block',
                    action='store',
                    default=False,
                    dest='block',
                    help='Takes block name as input for filter'),
        make_option('-g', '--village',
                    action='store',
                    default=False,
                    dest='village',
                    help='Takes village name as input for filter'),
        make_option('-a', '--animator',
                    action='store',
                    default=False,
                    dest='animator',
                    help='Takes mediator name as input for filter'),
        make_option('-w', '--numScreening',
                    action='store',
                    default=False,
                    dest='numScreening',
                    help='Takes nScreening as true or false to decide its inclusion in dataframe'),
        make_option('-u', '--numAdoption',
                    action='store',
                    default=False,
                    dest='numAdoption',
                    help='Takes nAdoption as true or false to decide its inclusion in dataframe'),
    )
    # --- options list for command line ends here ---

    # Function accepts the inputs and pass it to handle_controller for further processing
    def handle(self, *args, **options):
        dlib = data_lib()
        result_dataframe = dlib.handle_controller(args, options)
        print "--------------COMMAND LINE FINAL RESULT---------------"
        print result_dataframe
        print "--------------COMMAND LINE GAME OVER-----------------"

