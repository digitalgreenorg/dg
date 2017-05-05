from dg.settings import *

import os

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

TEMPLATE_DIRS = os.path.join(PROJECT_ROOT, "templates")